"""
Fantastic job so far! Now, we're advancing to a more complex task in our course.
Consider a scenario where you are working in AWS with Python's boto3,
and you need to manage multiple environments. For this, you are required
to write a Python script that creates an AWS Session using specific credentials
and then creates both a resource and a client instance for DynamoDB using that session.
Additionally, you need to create resource and client instances with the default AWS Session.
Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located in the top right corner.
Keep in mind, however, that resetting will erase any code changes.
To preserve your code during a reset, consider copying it to the clipboard.

"""
import boto3

# TO DO: Create an AWS session with explicit credentials 'test' / 'test' and region 'us-west-2'
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
    region_name='us-west-2'
)
print('AWS Session created')

default_session = boto3.Session()
print('AWS Default Session created')

# TO DO: Create a DynamoDB resource based on the session
dynamoDB_resource = session.resource('dynamodb')
print('AWS dynamoDB_resource created')


# TO DO: Create a DynamoDB client based on the session
dynamoDB_client = session.client('dynamodb')
print('AWS dynamoDB_client created')


# TO DO: Create a default DynamoDB resource with the default session
dynamoDB_default_resource = default_session.resource('dynamodb')
print('AWS dynamoDB_default_resource created')


# TO DO: Create a default DynamoDB client with the default session
dynamoDB_default_client = default_session.client('dynamodb')
print('AWS dynamoDB_default_client created')

