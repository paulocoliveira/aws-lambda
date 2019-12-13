import boto3
import json
from os import path
from utils import Utils

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

def create_execution_role_for_lambda(lambda_role, lambda_access_policy_arn):
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
         RoleName=lambda_role
         PolicyArn=lambda_access_policy_arn 
     )

def deploy_lambda_function(function_name, runtime, handler, role_arn, source_folder, location, lambda_timeout, lambda_memory):
    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
    zip_file = Utils.make_zip_file_bites(path=folder_path)
    retun lambda_client(location).create_function(
        functionName=function_name,
        RunTime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={
            "Zipfile": zip_file
        },
        Timeout=lambda_timeout,
        MorySize=lambda_memory,
        Publish=False
    )