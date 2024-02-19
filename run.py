import json
import os
import requests
import base64
import boto3


class Env0Settings:
    def __init__(
        self,
    ):
        self.api_key = os.getenv('ENV0_API_KEY')
        self.api_secret = os.getenv('ENV0_API_SECRET')
        self.organization_id = os.getenv('ENV0_ORGANIZATION_ID')
        #self.environment_id = os.getenv('ENV0_ENVIRONMENT_ID')
        #self.apikeysecret_encoded = os.getenv('TF_TOKEN_backend_api_env0_com')
        #if self.apikeysecret_encoded == '' and (self.api_secret == '' or self.api_key == ''):
        #    print(
        #        'Error: ENV0_API_KEY, ENV0_API_SECRET or TF_TOKEN_backend_api_env0_com not found; '
        #        'please remember to set either the key and secret or the token'
        #    )
        #elif self.apikeysecret_encoded == '':
        #    self.apikeysecret_encoded = base64.b64encode(
        #        f'{self.api_key}:{self.api_secret}'.encode()
        #    ).decode()
            
import requests


class HttpClient:
    def send_request(
        self,
        method,
        url,
        headers,
        params=None,
    ):
        if not params:
            
            params={}
        try:
            response = method(
                url=url,
                headers=headers,
                json=params,
            )
            response.raise_for_status()
        except Exception as e:
            raise e
        else:

            return response

class Env0ApiClient(
    HttpClient,
):
    base_url = 'https://api.env0.com'
    
    def __init__(
        self,
        api_key,
        api_secret,
        org_id,
    ):
        session = requests.session()
        session.auth = requests.auth.HTTPBasicAuth(
            username=api_key,
            password=api_secret,
        )

        self.session = session
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        
    def env0_api_call(
        self,
    ):
        pass
    
def extract_secret_key(
    my_string,
):
    return my_string.replace('${kosta_ssm:', '').replace('}', '')


def get_secret_from_secret_manager_by_secret_name(
    secret_name,
):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    secret = get_secret_value_response['SecretString']
    
    return secret
 

if __name__ == '__main__':
    
    with open('env0.env-vars.json', 'r') as f:
        file = json.load(f)
        
        
    retrieved_secrets = {}
    for key, value in file.items():
        if value.startswith('${kosta_ssm'):
            print(key, extract_secret_key(value))
            retrieved_secrets[key] = extract_secret_key(value)
            
            secret_from_ssm = get_secret_from_secret_manager_by_secret_name(extract_secret_key(value))
            
    
    env0_settings = Env0Settings()
    env0_client = Env0ApiClient(
        api_key=env0_settings.api_key,
        api_secret=env0_settings.api_secret,
        org_id=env0_settings.organization_id,
    )
