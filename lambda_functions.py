import boto3
import json
from os import path
from utils import Utils
import time

def lambda_client(location):
    aws_lambda = boto3.client('lambda', region_name=location)
    """ :type : pyboto3.lambda """
    return aws_lambda

def iam_client():
    iam = boto3.client('iam')
    """ :type : pyboto3.iam """
    return iam

def create_access_policy_for_lambda():
    s3_access_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "s3:*",
                    "logs:CreateLogGroup",
                    "Logs:CreateLogStream",
                    "Logs:PutLogEvents"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }

    return iam_client().create_policy(
        PolicyName='LambdaS3AccessPolicy',
        PolicyDocument=json.dumps(s3_access_policy_document),
        Description="Allows lambda function to access S3 resources."
    )

def create_execution_role_for_lambda(lambda_role):
    lambda_execution_assumption_role = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    return iam_client().create_role(
        RoleName=lambda_role,
        AssumeRolePolicyDocument=json.dumps(lambda_execution_assumption_role),
        Description="Gives necessary permissions for lambda to be executed"
    )

def attach_access_policy_to_execution_role(lambda_role, lambda_access_policy_arn):
     return iam_client().attach_role_policy(
         RoleName=lambda_role,
         PolicyArn=lambda_access_policy_arn 
     )

def deploy_lambda_function(function_name, runtime, handler, role_arn, source_folder, location, lambda_timeout, lambda_memory):
    time.sleep(10)
    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
    zip_file = Utils.make_zip_file_bytes(path=folder_path)
    return lambda_client(location).create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={
            "ZipFile": zip_file
        },
        Timeout=lambda_timeout,
        MemorySize=lambda_memory,
        Publish=False
    )

def invoke_lambda_function(location, function_name):
    return lambda_client(location).invoke(FunctionName=function_name)

def add_environment_variables_to_lambda(location, function_name, variables):
    return lambda_client(location).update_function_configuration(
        FunctionName=function_name,
        Environment=variables
    )

def update_lambda_function_code(location, funcion_name, source_folder):
    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
    zip_file = Utils.make_zip_file_bytes(path=folder_path)
    return lambda_client(location).update_function_code(
        FunctionName=funcion_name,
        ZipFile=zip_file
    )

def publish_a_new_version(location, function_name):
    return lambda_client(location).publish_version(
        FunctionName=function_name
    )

def create_alias_for_new_version(location, function_name, alias_name, version):
    return lambda_client(location).create_alias(
        FunctionName=function_name,
        Name=alias_name,
        FunctionVersion=version,
        Description="This is the " + alias_name + " alias for function " + function_name
    )

def invoke_lambda_with_alias(location, function_name, alias_name):
    return lambda_client(location).invoke(
        FunctionName=function_name,
        Qualifier=alias_name
    )

def get_function(location, function_name):
    return lambda_client(location).get_function(
        FunctionName=function_name
    )

def get_all_functions(location):
    return lambda_client(location).list_functions()

def increase_lambda_execution_memory(location, funcion_name, new_memory_size):
    return lambda_client(location).update_function_configuration(
        FunctionName=funcion_name,
        MemorySize=new_memory_size
    )

def delete_lambda_function(location, funcion_name):
    return lambda_client(location).delete_function(
        FunctionName=funcion_name
    )