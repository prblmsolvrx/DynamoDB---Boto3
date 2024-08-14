"""
DynamoDB's Scan operation, which reads every item in a table or those that meet specific criteria.
This operation can be particularly useful when you need to examine a broad dataset without prior
knowledge of the keys. Your task is to modify an existing Python script that creates a DynamoDB
table named Movies and populates it with records. Each movie record includes a genre attribute.
You are to adjust the Scan operation in the script to filter for movies in the Action genre
that were filmed after 2017. This will demonstrate how to refine Scan operations to retrieve
specific data efficiently.

Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located in the top right corner.
However, keep in mind that resetting will erase any code changes. To preserve your code during a reset,
consider copying it to the clipboard.
"""

import boto3
from boto3.dynamodb.conditions import Attr

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table
table = dynamodb.create_table(
    TableName='Movies',
    KeySchema=[
        {'AttributeName': 'year', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'title', 'KeyType': 'RANGE'}  # Sort key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'year', 'AttributeType': 'N'},
        {'AttributeName': 'title', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
)

# Wait for the table to be created, polling every 2 seconds and stopping after 10 attempts.
dynamodb.meta.client.get_waiter('table_exists').wait(
    TableName='Movies',
    WaiterConfig={
        'Delay': 2,
        'MaxAttempts': 10
    }
)

# Populate table with data including the genre attribute
table.put_item(Item={'year': 2016, 'title': 'The Big New Movie', 'genre': 'Comedy'})
table.put_item(Item={'year': 2017, 'title': 'The Bigger, Newer Movie', 'genre': 'Action'})
table.put_item(Item={'year': 2017, 'title': 'Yet Another Movie', 'genre': 'Action'})
table.put_item(Item={'year': 2017, 'title': 'One More Movie', 'genre': 'Drama'})
table.put_item(Item={'year': 2015, 'title': 'An Old Movie', 'genre': 'Romance'})
table.put_item(Item={'year': 2018, 'title': 'Another New Movie', 'genre': 'Action'})

# TODO: Modify the scan operation to filter for action movies filmed after 2017
response_scan = table.scan(
    FilterExpression=Attr('genre').eq('Action') & Attr('year').gt(2017)
)
print("Scan Results for 'Drama' Movies:", response_scan['Items'])