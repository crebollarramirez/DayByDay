import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import os
from dotenv import load_dotenv 

load_dotenv()

# Configure AWS settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DYNAMODB_TABLE_NAME = os.getenv("AWS_DYNAMODB_TABLE_NAME")

def create_dynamodb_table():
    # Create a DynamoDB client
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )

    # Define the table
    table_name = AWS_DYNAMODB_TABLE_NAME
    
    try:
        # Create the DynamoDB table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'content',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'content',
                    'AttributeType': 'S'  # String type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table is created
        table.wait_until_exists()
        print(f'Table {table_name} created successfully.')

    except ClientError as e:
        print(f'Error creating table: {e.response["Error"]["Message"]}')

    return table_name

def add_sample_item(table_name):
    # Create a DynamoDB client
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )

    table = dynamodb.Table(table_name)

    # Sample item data
    item = {
        'content': 'Take dog out for a walk',
    }

    try:
        # Add item to the table
        table.put_item(Item=item)
        print('Sample item added successfully.')

    except ClientError as e:
        print(f'Error adding item: {e.response["Error"]["Message"]}')

if __name__ == '__main__':
    table_name = create_dynamodb_table()
    add_sample_item(table_name)
