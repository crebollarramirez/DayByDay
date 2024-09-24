import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

# Configure AWS settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DYNAMODB_TABLE_NAME = os.getenv("AWS_DYNAMODB_TABLE_NAME")

# Initialize a session using your credentials
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

# Get the DynamoDB table
table = dynamodb.Table(AWS_DYNAMODB_TABLE_NAME)

def clear_table():
    # Scan the table to get all items
    response = table.scan()
    items = response['Items']

    # Delete each item
    for item in items:
        table.delete_item(
            Key={
                'content': item['content']  # Use the correct key name
            }
        )
    
    print(f"Deleted {len(items)} items from {AWS_DYNAMODB_TABLE_NAME}.")

    # Handle pagination if there are more items
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items = response['Items']
        
        for item in items:
            table.delete_item(
                Key={
                    'taskId': item['taskId']  # Use the correct key name
                }
            )
        
        print(f"Deleted {len(items)} additional items.")

if __name__ == "__main__":
    clear_table()