"""
You will begin with a template that already includes scripts for creating a DynamoDB table
named Movies and populating it with several records. Your focus will be on expanding
this script to include data retrieval operations using GetItem and BatchGetItem.
Specifically, you will demonstrate different retrieval strategies including simple reads,
reads with projection, and ensuring strongly consistent reads.
Important Note: Keep in mind that running scripts can modify the resources
in our AWS simulator. If you need to revert your AWS environment to its initial state,
use the reset button located in the top right corner of the simulator interface.
However, resetting the environment will remove any code changes you've made during your session.
To avoid losing your work, remember to save your code externally before hitting the reset button.
"""

import boto3

# Create DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='Movies',
    KeySchema=[
        { 'AttributeName': 'year', 'KeyType': 'HASH' }, # Partition key
        { 'AttributeName': 'title', 'KeyType': 'RANGE' } # Sort key
    ],
    AttributeDefinitions=[
        { 'AttributeName': 'year', 'AttributeType': 'N' },
        { 'AttributeName': 'title', 'AttributeType': 'S' },
    ],
    ProvisionedThroughput={ 'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5 }
)

# Wait for table to be created with custom waiter
table.meta.client.get_waiter('table_exists').wait(
    TableName='Movies', 
    WaiterConfig={
        'Delay': 2,           # Poll every 2 seconds
        'MaxAttempts': 10     # Make maximum 10 attempts
    }
)

# Insert movies into the table
table.put_item(Item={'year': 2016, 'title': 'The Big New Movie'})
table.put_item(Item={'year': 2017, 'title': 'The Bigger, Newer Movie'})
table.put_item(Item={'year': 2017, 'title': 'Yet Another Movie'})
table.put_item(Item={'year': 2017, 'title': 'One More Movie'})
table.put_item(Item={'year': 2015, 'title': 'An Old Movie'})
table.put_item(Item={'year': 2018, 'title': 'Another New Movie'})

# TODO: Retrieve 'The Big New Movie' from 2016 using a simple GetItem.
# TODO: Retrieve 'The Big New Movie' from 2016 using GetItem with ProjectionExpression for 'title' and 'genre'.
# TODO: Retrieve 'The Big New Movie' from 2016 using a strongly consistent read.
# TODO: Use BatchGetItem to retrieve 'The Big New Movie' from 2016 and 'The Bigger, Newer Movie' from 2017 with consistent read.

# Retrieve 'The Big New Movie' from 2016 using a simple GetItem.
response = table.get_item(
    Key={'year': 2016, 'title': 'The Big New Movie'}
)
item = response.get('Item')
print("Simple GetItem:", item)

# GetItem with ProjectionExpression
response = table.get_item(
    Key={'year': 2016, 'title': 'The Big New Movie'},
    ProjectionExpression='title, genre'
)
item = response.get('Item')
print("GetItem with ProjectionExpression:", item)

# Strongly consistent read
response = table.get_item(
    Key={'year': 2016, 'title': 'The Big New Movie'},
    ConsistentRead=True
)
item = response.get('Item')
print("Strongly Consistent Read:", item)

# BatchGetItem to retrieve multiple items
response = dynamodb.batch_get_item(
    RequestItems={
        'Movies': {
            'Keys': [
                {'year': 2016, 'title': 'The Big New Movie'},
                {'year': 2017, 'title': 'The Bigger, Newer Movie'}
            ],
            'ConsistentRead': True
        }
    }
)
items = response.get('Responses').get('Movies', [])
print("BatchGetItem Results:", items)