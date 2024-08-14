"""
Great progress! Now that you're familiar with DynamoDB basics,
it's time to dive into a practical coding exercise.
In this task, we have pre-provided a script for you.
Initially, this script sets up a DynamoDB table named Students.
Following the table creation, your primary task is to
utilize the batch_writer() function to add three student
records simultaneously. Each record should contain the
attributes: student_id, name, age, and major.

Important Note: Running scripts can modify the resources
in our AWS simulator. To revert to the initial state,
you can use the reset button located in the top right corner.
However, keep in mind that resetting will erase any code changes.
To preserve your code during a reset, consider copying it to the clipboard.
"""

import boto3

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

# Use wait_until_exists to ensure that your code won’t run until the table creation completes
dynamodb.meta.client.get_waiter('table_exists').wait(
    TableName='Students',
    WaiterConfig={
        'Delay': 2,       # Poll every 2 seconds
        'MaxAttempts': 10  # Make a maximum of 10 attempts
    }
)

# TODO: Use the batch_writer function to add three student records to the table. 
with table.batch_writer() as batch:
    batch.put_item(Item={'student_id': 1, 'name': 'Emma', 'age': 23, 'major': 'Biology'})
    batch.put_item(Item={'student_id': 2, 'name': 'Liam', 'age': 22, 'major': 'Chemistry'})
    batch.put_item(Item={'student_id': 3, 'name': 'Liamad', 'age': 32, 'major': 'Physics'})



