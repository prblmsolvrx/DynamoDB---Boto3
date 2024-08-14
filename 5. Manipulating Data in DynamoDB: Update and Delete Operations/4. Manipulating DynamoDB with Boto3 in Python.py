"""
 Your task involves enhancing a provided script that initializes a
 table named UserPosts. You will need to update attributes of
 existing entries and perform deletions both individually and in batch mode,
 showcasing your ability to handle multiple types of database modifications efficiently.

Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located in the top right corner.
However, keep in mind that resetting will erase any code changes.
To preserve your code during a reset, consider copying it to the clipboard.
"""

import boto3
from botocore.config import Config

# Initialize the boto3 DynamoDB resource
dynamodb = boto3.resource('dynamodb')
print("DynamoDB resource initialized successfully.")

# Create table with username as HASH key and post_id as RANGE key
table = dynamodb.create_table(
    TableName='UserPosts',
    KeySchema=[
        {'AttributeName': 'username', 'KeyType': 'HASH'},
        {'AttributeName': 'post_id', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'username', 'AttributeType': 'S'},
        {'AttributeName': 'post_id', 'AttributeType': 'N'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)
print("Table UserPosts is being created.")

# Wait for table to be fully created
dynamodb.meta.client.get_waiter('table_exists').wait(
    TableName='UserPosts',
    WaiterConfig={
        'Delay': 2,  # Poll every 2 seconds
        'MaxAttempts': 10  # Stop after 20 seconds
    }
)
print("Table UserPosts is created and active.")

# Insert initial items into the table
table.put_item(Item={'username': 'John', 'post_id': 1, 'content': 'Hello World!'})
print("Initial item added: John's first post.")
table.put_item(Item={'username': 'John', 'post_id': 2, 'content': 'Another Post'})
print("Initial item added: John's second post.")
table.put_item(Item={'username': 'Anna', 'post_id': 1, 'content': 'First Post'})
print("Initial item added: Anna's first post.")

# TO DO: Update the content and last_modified date for John's first post
table.update_item(
    Key={'username': 'John', 'post_id': 1},
    UpdateExpression='SET content = :content, last_modified = :last_modified',
    ExpressionAttributeValues={
        ':content': 'Updated content!',
        ':last_modified': '2024-08-14'
    }
)
print("Updated John's first post.")

# TO DO: Delete John's second post conditionally if the content matches
table.delete_item(
    Key={'username': 'John', 'post_id': 2},
    ConditionExpression='content = :content',
    ExpressionAttributeValues={
        ':content': 'Another Post'
    }
)
print("Conditionally deleted John's second post.")

# TO DO: Batch delete John's first post and Anna's first post
with table.batch_writer() as batch:
    batch.delete_item(
        Key = {
            'username': 'John',
            'post_id': 1
        } 
    )
    batch.delete_item(
        Key = {
            'username': 'Anna',
            'post_id': 1
        }
    )