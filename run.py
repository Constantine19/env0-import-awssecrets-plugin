import os
import sys

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
                f'"{prefix}" - {key}:{value}'
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
    print('Reading variables from the environment')
    env0_variables = models.env0_settings.Env0Settings()
    
    env0_environment_variables_json_file_handler = handlers.file_handler.FileHandler(
        file_path=env0_variables.env0_env_path_json_file,
    )

    print('Retrieving variables from env0.env-vars.json')
    env0_environment_variables_json_data = env0_environment_variables_json_file_handler.read_json()
    
    print(f'Retrieving secrets with the prefix "{SECRET_PREFIX}" from "env0.env-vars.json" file')
    retrieved_secrets = get_secret_variables_by_prefix(
        variables=env0_environment_variables_json_data,
        prefix=SECRET_PREFIX,
        aws_region=SECRET_AWS_REGION,
    )
    if not retrieved_secrets:
        print('No secrets were retrieved')
        sys.exit(0)

    secrets_file_handler = handlers.file_handler.FileHandler(
        file_path=env0_variables.env0_env_path,
    )
    print("Writing secrets to ENV0_ENV")
    secrets_file_handler.write_secrets(retrieved_secrets)
    print("Successfully written secrets to ENV0_ENV")