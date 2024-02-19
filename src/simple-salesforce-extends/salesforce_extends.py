import json
import logging

import boto3
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceExpiredSession

logger = logging.getLogger(__name__)
secrets_client = boto3.client("secretsmanager")


class SalesforceClientCredential(Salesforce):
    """
    About:
        Extends for simple_salesforce.Salesforce with Load/Save Salesforce credentials from/to Secrets Manager.
        This class is used for Salesforce Client Login Flow.
    see: https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_client_credentials_flow.htm&type=5

    prepare:
        Create Secrets Manager Secret with following JSON format:
        {
            "Domain": "yourdomain.my",
            "ConsumerKey": "3MV.....",
            "ConsumerSecret": "1234ABCD...."
        }
    """

    def __init__(self, *args, credentials_secrets_manager_arn=None, **kwargs):
        """
        Args: credentials_secrets_manager_arn is requires
        """
        self.credentials_secrets_manager_arn = credentials_secrets_manager_arn
        logger.debug(f"Secrets Manager Arn: {self.credentials_secrets_manager_arn=}")
        if not self.credentials_secrets_manager_arn:
            raise RuntimeError("credentials_secrets_manager_arn is required.")

        self.load_credentials()

        # Use token if exists
        if self.credentials.get("SessionId") and self.credentials.get("Instance"):
            kwargs["session_id"] = self.credentials.get("SessionId")
            kwargs["instance"] = self.credentials.get("Instance")
        else:
            # Rewrite parameters for client login flow if token does not exist
            kwargs["domain"] = self.credentials.get("Domain")
            kwargs["consumer_key"] = self.credentials.get("ConsumerKey")
            kwargs["consumer_secret"] = self.credentials.get("ConsumerSecret")

        super().__init__(*args, **kwargs)

    def _refresh_session(self):
        """Override Salesforce._refresh_session()"""
        super()._refresh_session()

        # Save session_id and instance to Secrets Manager
        self.credentials["SessionId"] = self.session_id
        self.credentials["Instance"] = self.sf_instance
        self.save_credentials()

    def _call_salesforce(self, method, url, name="", **kwargs):
        """Override API call method, re-authenticate if session is expired and retry"""
        try:
            return super()._call_salesforce(method, url, name, **kwargs)
        except SalesforceExpiredSession:
            # re-authenticate if session is expired and retry
            logger.info("Session is expired. Re-authenticate and retry.")
            self.re_authenticate()
            return super()._call_salesforce(method, url, name, **kwargs)

    def re_authenticate(self):
        super().__init__(
            domain=self.credentials.get("Domain"),
            consumer_key=self.credentials.get("ConsumerKey"),
            consumer_secret=self.credentials.get("ConsumerSecret"),
        )

    def load_credentials(self):
        """
        load credentials from Secrets Manager
            dict: {
                'Domain': 'yourdomain.my',  # remove ".salesforce.com" at the tail of your "MyDomain".
                'ConsumerKey': '3MV.....',
                'ConsumerSecret': '1234ABCD....',
                'SessionId': '<authenticated token string>',
                'Instance': '<authenticated instance domain>'
            }
        """
        logger.info("Loading Credentials")
        secret_value = secrets_client.get_secret_value(
            SecretId=self.credentials_secrets_manager_arn
        )
        self.credentials = json.loads(secret_value["SecretString"])
        logger.debug(f"Secret: {self.credentials=}")
        logger.info("Loaded Credentials")

    def save_credentials(self):
        """
        save credentials to Secrets Manager
        """
        logger.info("Saving Credentials")
        secrets_client.put_secret_value(
            SecretId=self.credentials_secrets_manager_arn,
            SecretString=json.dumps(self.credentials),
        )
        logger.info("Saved Credentials")
