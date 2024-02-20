# simple-salesforce-extends

[![PyPI version](https://badge.fury.io/py/simple-salesforce-extends.svg)](https://badge.fury.io/py/simple-salesforce-extends)
[![badge](https://pepy.tech/badge/simple-salesforce-extends)](https://pepy.tech/projects/simple-salesforce-extends)

## About

This package extends the simple-salesforce package to support the use of AWS Secrets Manager to store the Salesforce credentials.  
API request with the stored token if hold the token.  
If the token is expired, re-authenticate and store the new token.  

## Required

* Python 3.11+
* simple-salesforce
* boto3

## Install

```
$ pip install simple-salesforce-extends
```

## Prepare

Create a secret in AWS Secrets Manager with the following format:

```json
{
    "Domain": "yourdomain.my",
    "ConsumerKey": "3MV.....",
    "ConsumerSecret": "1234ABCD...."
}
```


## Usage

```python
import boto3
from simple_salesforce_extends import SalesforceClientCredential

sfdc_credential_secrets_arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:your-secret-arn"
secrets_client = boto3.client("secretsmanager", region_name="us-east-1")

sf = SalesforceClientCredential(
    secrets_client=secrets_client,
    credentials_secrets_manager_arn=sfdc_credential_secrets_arn,
)

soql = "SELECT Id, Name FROM Account LIMIT 1"
result = sf.query(soql)
print(result["records"][0])
```


## Test

```
$ python -m unittest discover -s src/
```
