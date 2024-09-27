import os
import time
from dotenv import load_dotenv 
import boto3
from botocore.exceptions import ClientError
import argparse

load_dotenv()

# Configure AWS settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DYNAMODB_TABLE_NAME = os.getenv("AWS_DYNAMODB_TABLE_NAME")

# Initialize the DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

def delete_table():
    # Get the DynamoDB table
    table = dynamodb.Table(AWS_DYNAMODB_TABLE_NAME)
    
    # Delete the table
    table.delete()
    print(f"Deleting table {AWS_DYNAMODB_TABLE_NAME}...")
    
    # Wait until the table is deleted
    while True:
        try:
            table.wait_until_not_exists()
            print(f"Table {AWS_DYNAMODB_TABLE_NAME} deleted successfully.")
            break
        except Exception as e:
            print("Waiting for table to delete...")
            time.sleep(5)

def create_dynamodb_table():
    # Define the table
    table_name = AWS_DYNAMODB_TABLE_NAME

    try:
        # Create the DynamoDB table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "title", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "item_type", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "title", "AttributeType": "S"},  # String type
                {"AttributeName": "item_type", "AttributeType": "S"},  # String type
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        # Wait until the table is created
        table.wait_until_exists()
        print(f"Table {table_name} created successfully.")

    except ClientError as e:
        print(f'Error creating table: {e.response["Error"]["Message"]}')

    return table_name

def scan_table(table_name):
    items = []
    table = dynamodb.Table(table_name)  # Use the resource object here
    
    response = table.scan()
    
    while True:
        items.extend(response.get('Items', []))
        
        # Check if there are more items to fetch
        if 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        else:
            break

    return items


def show():
    # List DynamoDB tables
    tables = dynamodb.tables.all()  # Change to use the resource for listing tables
    print('Tables:', [table.name for table in tables])  # Print names of the tables

    # Print all items in each table
    for table in tables:
        print(f"\nTable: {table.name}")
        items = scan_table(table.name)  # Now this function is defined before being called
        
        # Print each item and its attributes
        for item in items:
            print(item)
            print()

# parser = argparse.ArgumentParser(description="DB Help")
# parser.add_argument("--e", type=str, help="Refresh Databases")
# parser.add_argument("--s", type=str, help="Show all database information")

# args = parser.parse_args()

# if args.e is not None:
#     if args.e == "d":
#         delete_table()
#     if args.e == "s":
#         show()

show()





