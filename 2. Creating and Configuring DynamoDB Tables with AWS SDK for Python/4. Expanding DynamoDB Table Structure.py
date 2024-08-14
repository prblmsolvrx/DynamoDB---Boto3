import boto3
from botocore.exceptions import ClientError

# Initialize a boto3 resource for DynamoDB
dynamodb = boto3.resource('dynamodb')

try:
    # Create a DynamoDB table with ProductId as the partition key and Manufacturer as the range key
    table = dynamodb.create_table(
        TableName='Products',
        KeySchema=[
            {
                'AttributeName': 'ProductId',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Manufacturer',
                'KeyType': 'RANGE'  # Range key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ProductId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Manufacturer',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    # Implement a waiter to ensure the table is fully created
    waiter = dynamodb.meta.client.get_waiter('table_exists')
    waiter.wait(TableName='Products', WaiterConfig={'Delay': 2, 'MaxAttempts': 10})

    print("Table created successfully.")

except ClientError as e:
    print(f"An error occurred: {e}")

# List all DynamoDB tables to confirm the table creation
try:
    tables = dynamodb.tables.all()
    print("Listing all tables:")
    for table in tables:
        print(table.name)
except ClientError as e:
    print(f"An error occurred while listing tables: {e}")
