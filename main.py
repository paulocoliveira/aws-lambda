from lambda_functions import lambda_client, iam_client, create_access_policy_for_lambda, create_execution_role_for_lambda, attach_access_policy_to_execution_role, deploy_lambda_function, invoke_lambda_function, add_environment_variables_to_lambda, update_lambda_function_code, publish_a_new_version, create_alias_for_new_version, invoke_lambda_with_alias, get_function, get_all_functions, increase_lambda_execution_memory, delete_lambda_function

LOCATION = "us-east-1"
LAMBDA_ACCESS_POLICY_ARN = ""
LAMBDA_ROLE = "Lambda_Execution_Role"
LAMBDA_ROLE_ARN = ""
LAMBDA_TIMEOUT = 10
LAMBDA_MEMORY = 128
LAMBDA_HANDLER = "lambda_function.handler"
PYTHON_36_RUNTIME = "python3.6"
PYTHON_LAMBDA_NAME = "PythonLambdaFunction"

print(lambda_client(LOCATION))
policy_response = create_access_policy_for_lambda()
print(policy_response)
LAMBDA_ACCESS_POLICY_ARN = policy_response['Policy']['Arn']
role_response = create_execution_role_for_lambda(LAMBDA_ROLE)
print(role_response)
LAMBDA_ROLE_ARN = role_response['Role']['Arn']
print(attach_access_policy_to_execution_role(LAMBDA_ROLE, LAMBDA_ACCESS_POLICY_ARN))

print(deploy_lambda_function(PYTHON_LAMBDA_NAME, PYTHON_36_RUNTIME, LAMBDA_HANDLER, LAMBDA_ROLE_ARN, "python_lambda", LOCATION, LAMBDA_TIMEOUT, LAMBDA_MEMORY))

response = invoke_lambda_function(LOCATION, PYTHON_LAMBDA_NAME)
print(response['Payload'].read().decode())

env_variables={
    "Variables":{
        "ENV_VAR_TEST": "This is an environment variable!"
    }
}

add_environment_variables_to_lambda(LOCATION, PYTHON_LAMBDA_NAME, env_variables)

print(update_lambda_function_code(LOCATION, PYTHON_LAMBDA_NAME, "python_lambda"))
response = invoke_lambda_function(LOCATION, PYTHON_LAMBDA_NAME)
print(response['Payload'].read().decode())

print(publish_a_new_version(LOCATION, PYTHON_LAMBDA_NAME))

create_alias_for_new_version(LOCATION, PYTHON_LAMBDA_NAME, "PROD", "1")

response = invoke_lambda_with_alias(LOCATION, PYTHON_LAMBDA_NAME, "PROD")
print(response['Payload'].read().decode())

print(get_function(LOCATION, PYTHON_LAMBDA_NAME))

print(get_all_functions(LOCATION))

increase_lambda_execution_memory(LOCATION, PYTHON_LAMBDA_NAME, 256)

delete_lambda_function(LOCATION, PYTHON_LAMBDA_NAME)