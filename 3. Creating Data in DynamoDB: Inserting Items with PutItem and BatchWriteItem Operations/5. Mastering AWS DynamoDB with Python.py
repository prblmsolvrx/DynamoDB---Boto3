"""
interact with an existing AWS DynamoDB table named Students,
which already has student_id as the primary key. Populate
this table with a few records, ensuring each record includes
student_id, name, age, and major. Utilize conditional expressions
to prevent overwriting existing records. Lastly, query and print
all items from the Students table.
Ready to take on the challenge? Remember all the skills and knowledge
you've acquired so far, and good luck!
Important Note: Running scripts can modify the resources
in our AWS simulator. To revert to the initial state, you can
use the reset button located in the top right corner. However, keepin mind that resetting will erase any code changes. To preserve your code during a reset, consider copying it to the clipboard.
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

# Wait for the table to be created
dynamodb.meta.client.get_waiter('table_exists').wait(
    TableName='Students', 
    WaiterConfig={
        'Delay': 2, 
        'MaxAttempts': 10
    }
)

# TO DO: Add a student item to the table
# TO DO: Use a BatchWriteItem operation to add multiple student items to the table
# TO DO: Try to add another item with the same primary key as an existing item using a condition expression to avoid overwriting
# TO DO: List and print all items in the created table
# Add a single student item to the table
# Add a single student item to the table

with table.batch_writer() as batch:
    batch.put_item(
        Item={
            'student_id': 1,
            'name': 'Emma',
            'age': 23,
            'major': 'Biology'
        }
    )

# Use a BatchWriteItem operation to add multiple student items
with table.batch_writer() as batch:
    batch.put_item(
        Item={
            'student_id': 2,
            'name': 'Liam',
            'age': 22,
            'major': 'Chemistry'
        }
    )
    batch.put_item(
        Item={
            'student_id': 3,
            'name': 'Liamad',
            'age': 32,
            'major': 'Physics'
        }
    )

# Try to add another item with the same primary key as an existing item
table.put_item(
    Item={
        'student_id': 1,
        'name': 'Emma Updated',
        'age': 24,
        'major': 'Biology'
    },
    ConditionExpression='attribute_not_exists(student_id)'
)

# List and print all items in the created table
response = table.scan()
items = response.get('Items', [])

for item in items:
    print(item)