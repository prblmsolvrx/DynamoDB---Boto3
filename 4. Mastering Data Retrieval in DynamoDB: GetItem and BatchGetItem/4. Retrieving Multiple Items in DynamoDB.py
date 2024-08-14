"""
 You have a script that builds a table named Movies and populates
 it with a few records. Each record represents a movie,
 containing attributes such as year and title.
 Your objective is to extend the functionality of
 this script by adding data retrieval operations to fetch
 movies from the table. Specifically, you must
 add the batch_get_item operation to retrieve
 two movies simultaneously: 'The Big New Movie' from 2016 and 'The Bigger, Newer Movie' from 2017.
Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located in the top right corner. However,
keep in mind that resetting will erase any code changes.
To preserve your code during a reset, consider copying it to the clipboard.
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
    Key={
        'year': 2016,
        'title': 'The Big New Movie'
    }
)
item = response.get('Item')
print("Simple GetItem:", item)

# Retrieve 'The Big New Movie' from 2016 using GetItem with ProjectionExpression for 'title' (and 'genre' if it existed).
response = table.get_item(
    Key={
        'year': 2016,
        'title': 'The Big New Movie'
    },
    ProjectionExpression='title'  # Adjust if you have other attributes
)
item = response.get('Item')
print("GetItem with ProjectionExpression:", item)

# Retrieve 'The Big New Movie' from 2016 using a strongly consistent read.
response = table.get_item(
    Key={
        'year': 2016,
        'title': 'The Big New Movie'
    },
    ConsistentRead=True
)
item = response.get('Item')
print("Strongly Consistent Read:", item)

# Use BatchGetItem to retrieve 'The Big New Movie' from 2016 and 'The Bigger, Newer Movie' from 2017 with consistent read.
response = client.batch_get_item(
    RequestItems={
        'Movies': {
            'Keys': [
                {'year': {'N': '2016'}, 'title': {'S': 'The Big New Movie'}},
                {'year': {'N': '2017'}, 'title': {'S': 'The Bigger, Newer Movie'}}
            ],
            'ConsistentRead': True
        }
    }
)
items = response.get('Responses', {}).get('Movies', [])
print("BatchGetItem Results:", items)