import json
import unittest
import unittest.mock

from simple_salesforce_extends.salesforce_extends import SalesforceClientCredential


class SecretsManager(unittest.mock.Mock):
    def get_secret_value(self, SecretId):
        return {
            "SecretString": json.dumps(
                {
                    "Domain": "yourdomain.my",  # remove ".salesforce.com" at the tail of your "MyDomain".
                    "ConsumerKey": "3MV.....ZZZ",
                    "ConsumerSecret": "1234ABCD....ZZZ",
                    "SessionId": "12345",
                    "Instance": "yourdomain.my.salesforce.com",
                }
            )
        }


class SalesforceCredentialTests(unittest.TestCase):
    def test_salesforce_credential_constructor_normal(self):
        secrets_client = SecretsManager()  # mock
        arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:SalesforceCredentialTest"
        sf = SalesforceClientCredential(
            secrets_client=secrets_client, credentials_secrets_manager_arn=arn
        )
        self.assertIsInstance(sf, SalesforceClientCredential)

    def test_salesforce_credential_constructor_exception(self):
        secrets_client = None
        arn = ""

        with self.assertRaises(RuntimeError):
            SalesforceClientCredential(
                secrets_client=secrets_client, credentials_secrets_manager_arn=arn
            )

        secrets_client = SecretsManager()  # mock
        arn = ""
        with self.assertRaises(RuntimeError):
            SalesforceClientCredential(
                secrets_client=secrets_client, credentials_secrets_manager_arn=arn
            )

        secrets_client = None
        arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:SalesforceCredentialTest"
        with self.assertRaises(RuntimeError):
            SalesforceClientCredential(
                secrets_client=secrets_client, credentials_secrets_manager_arn=arn
            )
