"""
As a first step into DynamoDB, you are tasked with reading the provided Python script.
This script uses the Python SDK Boto3 to interact with DynamoDB and to create a table
named Users. Additionally, the script utilizes the resource interface of Boto3 to
create the DynamoDB table and employs the wait_until_exists method without parameters
to pause execution until the table is ready. No coding is required for this task;
simply review the script, understand its functionality, and then execute it.
Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located in the top
right corner. However, keep in mind that resetting will erase any code changes.
To preserve your code during a reset, consider copying it to the clipboard.
"""

import boto3
from botocore.config import Config

# Initialize the boto3 resource for DynamoDB
dynamodb = boto3.resource('dynamodb')

# Create the 'Users' table
table = dynamodb.create_table(
    TableName='Users',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait for the table to exist without specifying additional parameters
table.wait_until_exists()

print("Table 'Users' has been created.")