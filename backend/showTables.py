import os
from dotenv import load_dotenv 
import boto3

load_dotenv()

# Configure AWS settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DYNAMODB_TABLE_NAME = os.getenv("AWS_DYNAMODB_TABLE_NAME")

# Initialize the DynamoDB client
dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

# Function to scan a table and get all items
def scan_table(table_name):
    items = []
    table = boto3.resource('dynamodb', region_name=AWS_REGION_NAME).Table(table_name)
    
    response = table.scan()
    
    while True:
        items.extend(response.get('Items', []))
        
        # Check if there are more items to fetch
        if 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        else:
            break

    return items

# List DynamoDB tables
tables = dynamodb.list_tables()
print('Tables:', tables['TableNames'])

# Print all items in each table
for table_name in tables['TableNames']:
    print(f"\nTable: {table_name}")
    items = scan_table(table_name)
    
    # Print each item and its attributes
    for item in items:
        print(item)
        print()
