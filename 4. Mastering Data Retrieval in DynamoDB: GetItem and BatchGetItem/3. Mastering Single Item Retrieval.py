"""
enhance a Python script that already creates a DynamoDB table named Movies and populates
it with several movie records. Your objective is to refine this script by implementing
read operations that retrieve specific movie details using their primary keys.
You will modify the script to retrieve details for two movies: 'The Big New Movie' from 2016,
and 'The Bigger, Newer Movie' from 2017. For the second movie, ensure you only
retrieve the title by using a projection. After modifying the script, run it to
observe how DynamoDB fetches and displays these records.

Important Note: Running scripts can modify resources in our AWS simulator.
To revert to the initial state, you can use the reset button located
in the top right corner. Keep in mind that resetting will erase any code changes.
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
        { 'AttributeName': 'title', 'KeyType': 'RANGE' }  # Sort key
    ],
    AttributeDefinitions=[
        { 'AttributeName': 'year', 'AttributeType': 'N' },
        { 'AttributeName': 'title', 'AttributeType': 'S' },
    ],
    ProvisionedThroughput={ 'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5 }
)

# Wait for the table to be created or until 20 seconds have passed
dynamodb.meta.client.get_waiter('table_exists').wait(
    TableName='Movies',
    WaiterConfig={
        'Delay': 2,  # Poll every 2 seconds
        'MaxAttempts': 10  # Stop after 20 seconds
    }
)

# Insert movies into the table
table.put_item(Item={'year': 2016, 'title': 'The Big New Movie'})
table.put_item(Item={'year': 2017, 'title': 'The Bigger, Newer Movie'})

# TODO: Add the GetItem operation to retrieve the first movie using its primary key
response1 = table.get_item(
    Key={
        'year': 2016,
        'title': 'The Big New Movie'
    }
)
first_movie = response1.get('Item')
print('First Movie:', first_movie)

# TODO: Add the GetItem operation with ProjectionExpression to retrieve only the "title" attribute of the second movie
# Retrieve the second movie with ProjectionExpression to get only the "title" attribute
response2 = table.get_item(
    Key={
        'year': 2017,
        'title': 'The Bigger, Newer Movie'
    },
    ProjectionExpression='title'
)
second_movie_title = response2.get('Item')
print('Second Movie Title:', second_movie_title)