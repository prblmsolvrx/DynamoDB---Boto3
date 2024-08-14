"""
modifying an existing query. Initially, it fetches movies from a specific year.
Adjust it to retrieve only the movies from 2016 with titles starting with "The".
This modification will showcase the power and flexibility of key conditions in
narrowing down search results.

Important Note: Running scripts can lead to alterations in our AWS simulator resources.
To return to the starting state, use the reset button in the top right corner.
Be aware, resetting will erase any code changes. To safeguard your code during a reset,
consider copying it to the clipboard.
"""

import boto3
from boto3.dynamodb.conditions import Key

# Initiate a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Build the DynamoDB table
table = dynamodb.create_table(
    TableName='Movies',
    KeySchema=[
        {'AttributeName': 'year', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'title', 'KeyType': 'RANGE'}  # Sort key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'year', 'AttributeType': 'N'},
        {'AttributeName': 'title', 'AttributeType': 'S'},
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
)

# Wait until the table is fully created
dynamodb.meta.client.get_waiter('table_exists').wait(TableName='Movies', WaiterConfig={'Delay': 2, 'MaxAttempts': 10})

# Fill the table with data
table.put_item(Item={'year': 2016, 'title': 'The Big New Movie'})
table.put_item(Item={'year': 2016, 'title': 'The Bigger, Newer Movie'})
table.put_item(Item={'year': 2016, 'title': 'Yet Another Movie'})
table.put_item(Item={'year': 2018, 'title': 'One More Movie'})

# Example with Query Command
# TODO: Modify this query to filter only movies from 2016 that start with 'The'
response_query = table.query(
    KeyConditionExpression=Key('year').eq(2016) & Key('title').begins_with('The')
)
print("Query Results:", response_query['Items'])