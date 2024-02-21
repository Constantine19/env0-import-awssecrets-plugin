import botocore

from . import _boto3_client


class AwsSecretsManagerApiClient(
    _boto3_client.Boto3Client,
):
    service_name = 'secretsmanager'
    
    def __init__(
        self,
        region,
    ):
        self.region = region
        self.client = self.get_session(
            service_name=self.service_name,
            region_name=self.region
        )
        
    def get_secret_value_by_key(
        self,
        secret_key,
    ):
        print(
            f'Getting a secret by key "{secret_key}"'
        )
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_key
            )
        except botocore.exceptions.ClientError as e:
            raise(e)
        else:
            secret = get_secret_value_response['SecretString']
            
        return secret
