"""
enhance your understanding of the Scan operation,
which allows for comprehensive data retrieval across a DynamoDB table.
The table, named Movies, already contains multiple movie records,
each with attributes like year, title, and genre. Your challenge
is to implement several Scan operations ranging from simple to
complex to filter movies based on different criteria.
This exercise aims to showcase the versatility and broad applicability
of the Scan operation compared to the Query operation.
Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located
in the top right corner. However, keep in mind that resetting will erase any code changes.
To preserve your code during a reset, consider copying it to the clipboard.
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

# Wait for the table to be created
dynamodb.meta.client.get_waiter('table_exists').wait(
    TableName='Movies',
    WaiterConfig={
        'Delay': 2,  # poll every 2 seconds
        'MaxAttempts': 10  # maximum 10 attempts
    }
)

# Populate table with data including the genre attribute
table.put_item(Item={'year': 2016, 'title': 'The Big New Movie', 'genre': 'Comedy'})
table.put_item(Item={'year': 2017, 'title': 'The Bigger, Newer Movie', 'genre': 'Action'})
table.put_item(Item={'year': 2017, 'title': 'Yet Another Movie', 'genre': 'Action'})
table.put_item(Item={'year': 2017, 'title': 'One More Movie', 'genre': 'Drama'})
table.put_item(Item={'year': 2015, 'title': 'An Old Movie', 'genre': 'Romance'})
table.put_item(Item={'year': 2018, 'title': 'Another New Movie', 'genre': 'Action'})

# TODO: Write a simple Scan operation to find all movies.
# TODO: Write a Scan operation to find all 'Action' movies.
# TODO: Write a Scan operation to find all movies released after 2016.
# Simple Scan operation to find all movies

response_all_movies = table.scan()
print("All Movies:", response_all_movies['Items'])

# Scan operation to find all 'Action' movies
response_action_movies = table.scan(
    FilterExpression=Attr('genre').eq('Action')
)
print("Action Movies:", response_action_movies['Items'])

# Scan operation to find all movies released after 2016
response_movies_after_2016 = table.scan(
    FilterExpression=Attr('year').gt(2016)
)
print("Movies Released After 2016:", response_movies_after_2016['Items'])