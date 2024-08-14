"""
add one more student record to the table. Begin by reviewing the provided script,
and when you're ready, fill in the TODO line of code with a new student record,
adding another student named Emily Johnson with the details student_id: 2,
name: 'Emily Johnson', age: 22, and major: 'Data Science' to the Students table.
Please ensure your script runs without errors and successfully populates
the database with the new record.
Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located in the top right corner.
Keep in mind that resetting will erase any code changes. To preserve your code
during a reset, consider copying it to the clipboard.
"""

import boto3
import time

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table
table = dynamodb.create_table(
    TableName='Students',
    AttributeDefinitions=[
        {
            'AttributeName': 'student_id',
            'AttributeType': 'N'
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'student_id',
            'KeyType': 'HASH'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Waiting for the table to be created. Poll every 2 seconds for a maximum of 10 attempts
dynamodb.meta.client.get_waiter('table_exists').wait(TableName='Students', WaiterConfig={'Delay': 2, 'MaxAttempts': 10})

# Put a data item in the table with PutItem
table.put_item(
    Item={
        'student_id': 1,
        'name': 'John Doe',
        'age': 22,
        'major': 'Computer Science'
    }
)

# TODO: Add another student 'Emily Johnson' with details student_id: 2, age: 22 and major: 'Data Science'

table.put_item(
    Item={
        'student_id': 2,
        'name': 'Emily Johnson',
        'age': 22,
        'major': 'Data Science'
    }
)

# Listing all items in the created table
response = table.scan()

for item in response['Items']:
    print(item)