from lambda_functions import lambda_client, iam_client, create_access_policy_for_lambda, create_execution_role_for_lambda, attach_access_policy_to_execution_role, deploy_lambda_function

LOCATION = "us-east-1"
LAMBDA_ACCESS_POLICY_ARN = ""
LAMBDA_ROLE = "Lambda_Execution_Role"
LAMBDA_ROLE_ARN = ""
LAMBDA_TIMEOUT = 10
LAMBDA_MEMORY = 128
LAMNDA_HANDLER = "lambda_function.handler"
PYTHON_36_RUNTIME = "python3.6"
PYTHON_LAMBDA_NAME = "PythonLambdaFunction"

print(lambda_client(LOCATION))
print(create_access_policy_for_lambda())
print(create_execution_role_for_lambda(LAMBDA_ROLE))
print(attach_access_policy_to_execution_role(LAMBDA_ROLE, LAMBDA_ACCESS_POLICY_ARN))
print(deploy_lambda_function(PYTHON_LAMBDA_NAME, PYTHON_36_RUNTIME, LAMNDA_HANDLER, LAMBDA_ROLE_ARN, "python_lambda", LOCATION, LAMBDA_TIMEOUT, LAMBDA_MEMORY))