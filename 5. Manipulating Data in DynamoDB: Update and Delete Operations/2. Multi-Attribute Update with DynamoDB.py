"""
adjust an existing Python script aimed at creating a DynamoDB table named UserPosts,
inserting a few initial items into the table, and performing an update action on
the inserted items. Your specific task involves modifying the existing
update_item function to change not just the status but also the content
attribute of a particular post, represented by an item in the table.
Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located in the top right corner.
However, keep in mind that resetting will erase any code changes.
To preserve your code during a reset, consider copying it to the clipboard.
"""

import boto3
import time

# Initialize the boto3 DynamoDB resource
dynamodb = boto3.resource('dynamodb')
print("DynamoDB resource initialized.")

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
print("Table 'UserPosts' creation initiated.")

# Wait for table to be fully created
dynamodb.meta.client.get_waiter('table_exists').wait(
    TableName='UserPosts',
    WaiterConfig={
        'Delay': 2,  # Poll every 2 seconds
        'MaxAttempts': 10  # Stop after 20 seconds
    }
)
print("Table 'UserPosts' is active.")

# Insert initial items into the table
table.put_item(Item={'username': 'John', 'post_id': 1, 'content': 'Hello World!'})
print("Item inserted: John's first post.")
table.put_item(Item={'username': 'John', 'post_id': 2, 'content': 'Another Post'})
print("Item inserted: John's second post.")
table.put_item(Item={'username': 'Anna', 'post_id': 1, 'content': 'First Post'})
print("Item inserted: Anna's first post.")

# TODO: Modify following update to also change the content of John's first post along with the status.
table.update_item(
    Key={'username': 'John', 'post_id': 1},
    UpdateExpression='SET #sts = :val2, content = :newContent',
    ExpressionAttributeNames={'#sts': 'status'},
    ExpressionAttributeValues={
        ':val2': 'updated',
        ':newContent': 'Updated content of the post'
    }
)
print("John's first post status and content updated.")