# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/
import json

import boto3
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "AWS-ENCLAVE"
    region_name = "eu-central-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    response = json.loads(response["SecretString"])
    print("response:", response)
    print("type:", type(response))

    dot_env = {
        "OPEN_AI_API_KEY": response["OPEN_AI_API_KEY"],
        "SERPER_API_KEY": response["SERPER_API_KEY"],
        "WEB3_RPC_URL": response["WEB3_RPC_URL"]
    }
    print("\nDotEnv:")
    print(dot_env)
    _save_dot_env(dot_env)
    _save_gcp(response["SIDEKIK_AI"])
    # secret = get_secret_value_response['SecretString']
    # Your code goes here.


def _save_dot_env(dot_env):
    with open(".env", "w") as file:
        for key, value in dot_env.items():
            file.write(key + '="' + value + '"\n')


def _save_gcp(gcp):
    with open("sidekik.json", "w") as file:
        file.write(gcp)


if __name__ == '__main__':
    get_secret()
