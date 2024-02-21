import json
import os

import clients
import handlers
import models


SECRET_PREFIX = os.getenv('SECRET_PREFIX')
SECRET_AWS_REGION = os.getenv('SECRET_AWS_REGION')


def get_secret_variables_by_prefix(
    variables,
    prefix,
    aws_region,
):
    secret_variables_by_prefix = {}
    prefix_handler = handlers.prefix_handler.PrefixHandler(prefix)
    secrets_manager_client = clients.aws_secrets_manager_client.AwsSecretsManagerApiClient(
        region=aws_region,
    )
    for key, value in variables.items():
        if prefix_handler.is_prefixed(value):
            print(
                f'Found secret matching prefix '
                '"{prefix}" - {key}:{value}'
            )
            try:
                secret_key = prefix_handler.extract_secret_key(
                    prefix_embedded_value=value,
                )
                secret_value = secrets_manager_client.get_secret_value_by_key(secret_key)
                secret_variables_by_prefix[secret_key] = secret_value
            except Exception as e:
                print(
                    f'Error fetching secrets for {key}: {value}'
                    f'Message: {e}'
                )
            
    return secret_variables_by_prefix
    

if __name__ == '__main__':
    env0_variables = models.env0_settings.Env0Settings()
    
    env0_environment_variables_json_file_handler = handlers.file_handler.FileHandler(
        file_path=env0_variables.env0_env_path_json_file,
    )
    env0_environment_variables_json_data = env0_environment_variables_json_file_handler.read_json()
    
    retrieved_secrets = get_secret_variables_by_prefix(
        variables=env0_environment_variables_json_data,
        prefix=SECRET_PREFIX,
        aws_region=SECRET_AWS_REGION,
    )
    
    secrets_file_handler = handlers.file_handler.FileHandler(
        file_path=env0_variables.env0_env_path,
    )
    secrets_file_handler.write_secrets(
        retrieved_secrets,
    )
