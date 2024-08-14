"""
In your final task, you will synthesize what you have learned so far and write a script that creates two
DynamoDB tables — Users and Customers. For the Users table, you should use a provisioned capacity
mode with a read and write capacity of 5. For the Customers table, apply the on-demand capacity mode.
Each table should have only one attribute serving as a primary key: username in Users, and customer_id
in Customers. After successfully creating the tables, implement a command to display all of your
existing DynamoDB tables.

In this task, you will use wait_until_exists() for the Users table to automatically wait
for the table to become active. For the Customers table, configure a custom waiter object
to poll every 2 seconds and make a maximum of 10 attempts to check the status of the table.

Important Note: Running scripts can modify the resources in our AWS simulator.
To revert to the initial state, you can use the reset button located in the top right corner.
However, keep in mind that resetting will erase any code changes. To preserve your code during
a reset, consider copying it to the clipboard."""

import boto3
from botocore.exceptions import ClientError
from time import sleep

# Initialize the boto3 DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Create the 'Users' table with Provisioned Throughput and a primary key of 'username'
def create_users_table():
    try:
        table = dynamodb.create_table(
            TableName='Users',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Creating 'Users' table...")
        table.wait_until_exists()
        print("'Users' table created and exists.")
    except ClientError as e:
        print(f"Error creating 'Users' table: {e}")

# Create the 'Customers' table with On-Demand capacity and a primary key of 'customer_id'
def create_customers_table():
    try:
        table = dynamodb.create_table(
            TableName='Customers',
            KeySchema=[
                {
                    'AttributeName': 'customer_id',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'customer_id',
                    'AttributeType': 'S'
                },
            ],
            BillingMode='PAY_PER_REQUEST'  # On-Demand capacity mode
        )
        print("Creating 'Customers' table...")

        # Configure a custom waiter for the 'Customers' table
        waiter = dynamodb.meta.client.get_waiter('table_exists')
        max_attempts = 10
        interval = 2

        for attempt in range(max_attempts):
            try:
                waiter.wait(TableName='Customers')
                print("'Customers' table created and exists.")
                break
            except ClientError as e:
                print(f"Attempt {attempt + 1}/{max_attempts} failed: {e}")
                sleep(interval)
        else:
            print("Failed to confirm 'Customers' table creation.")
    except ClientError as e:
        print(f"Error creating 'Customers' table: {e}")

# List all the existing tables in DynamoDB
def list_tables():
    try:
        table_names = dynamodb.tables.all()
        print("Existing tables:")
        for table in table_names:
            print(table.name)
    except ClientError as e:
        print(f"Error listing tables: {e}")

# Execute the functions
create_users_table()
create_customers_table()
list_tables()
