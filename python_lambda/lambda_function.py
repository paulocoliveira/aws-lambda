import os

def handler(event, context):
    env_variables = os.getenv("ENV_VAR_TEST")
    return {
        "status_code": 200,
        "message": "Hello from Python Lambda Function!"
    }