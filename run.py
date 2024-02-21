import json
import re

import clients
import models

    
def extract_secret_key(
    prefix_embedded_value,
    prefix,
):
    pattern = rf'\$\{{{prefix}:(.*?)\}}'
    match = re.findall(pattern, prefix_embedded_value)

    return match

def get_env0_environment_variables(
    file_path,
):
    with open(file_path, 'r') as file:
        env0_environment_variables = json.load(file)
        
    return env0_environment_variables

def get_secret_variables_by_prefix(
    variables,
    prefix,
    aws_region,
):
    secrets = {}
    secrets_manager_client = clients.aws_secrets_manager_client.AwsSecretsManagerApiClient(
        region=aws_region,
    )
    
    for key, value in variables.items():
        if value.startswith(prefix):
            print(
                f'Found secret matching prefix "{prefix}" - {key}:{value}',
            )
            secret_key = extract_secret_key(
                prefix_embedded_value=value,
                prefix=prefix,
            )
            secret_value = secrets_manager_client.get_secret_value_by_key(secret_key)
            secrets[secret_key] = secret_value
            
    return secrets
    
def dump_secrets_into_environment_variables(
    file_path,
    secrets_data,
    env0_environment_variables
):
    with open(file_path, 'w+') as file:
        for key, value in secrets_data.items():
            file.write(f'{key}: {value}')
        #     env0_environment_variables[key] = value
        # json.dump(env0_environment_variables, file)
        # dump into env0_env only retrieved secrets


if __name__ == '__main__':
    env0_variables = models.env0_settings.Env0Settings()
    # import pydantic
    # class Env0Variables(pydantic.BaseModel):
    #     env0_env_path:  str = 'env0.env-vars.json'
        
    # env0_variables = Env0Variables()
    
    print(f'########### env0_variables {env0_variables} ############')
    
    print(f'########### env0_variables.env0_env_path {env0_variables.env0_env_path} ############')
    
    print(f'########### env0_variables.env0_env_path_json_file {env0_variables.env0_env_path_json_file} ############')
    
    env0_environment_variables = get_env0_environment_variables(
        file_path=env0_variables.env0_env_path_json_file,
    )
    retrieved_secrets = get_secret_variables_by_prefix(
        variables=env0_environment_variables,
        prefix='kosta_ssm',
        aws_region='us-east-1',
    )
    
    dump_secrets_into_environment_variables(
        file_path=env0_variables.env0_env_path,
        secrets_data=retrieved_secrets,
        env0_environment_variables=env0_environment_variables,
    )
