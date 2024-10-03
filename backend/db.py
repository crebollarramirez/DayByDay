import os
import time
from dotenv import load_dotenv 
import boto3
from botocore.exceptions import ClientError
import argparse
import bcrypt

load_dotenv()

# Configure AWS settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DYNAMODB_TABLE_NAME = os.getenv("AWS_DYNAMODB_TABLE_NAME")
AWS_DYNAMODB_TABLE_NAME2 = os.getenv("AWS_DYNAMODB_TABLE_NAME2")
# Initialize the DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
    endpoint_url='http://localhost:8080'  # For local DynamoDB instance
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

    table = dynamodb.Table(AWS_DYNAMODB_TABLE_NAME2)
    
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

    table_name = AWS_DYNAMODB_TABLE_NAME2

    try:
        # Create the DynamoDB table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "username", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "attribute_type", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "username", "AttributeType": "S"},  # String type
                {"AttributeName": "attribute_type", "AttributeType": "S"},  # String type
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

def addDummyData():
    Item1 = {
        "item_type": "FREQUENT",
        "title": "Morning Walk",
        "content": "Take the dog for a morning walk.",
        "frequency": "MONDAY",
        "completed": False,
        "timeFrame": ("7:00AM", "8:00AM")
    }

    Item2 = {
        "item_type": "FREQUENT",
        "title": "Team Check-In",
        "content": "Have a quick check-in with the team.",
        "frequency": "MONDAY",
        "completed": False,
        "timeFrame": ("11:00AM", "11:30AM")
    }

    Item3 = {
        "item_type": "FREQUENT",
        "title": "Grocery Shopping",
        "content": "Buy groceries for the week.",
        "frequency": "TUESDAY",
        "completed": False,
        "timeFrame": ("10:00AM", "11:00AM")
    }

    Item4 = {
        "item_type": "FREQUENT",
        "title": "Yoga Class",
        "content": "Attend a virtual yoga class.",
        "frequency": "TUESDAY",
        "completed": False,
        "timeFrame": ("6:00PM", "7:00PM")
    }

    Item5 = {
        "item_type": "FREQUENT",
        "title": "Weekly Meeting",
        "content": "Attend the project weekly meeting.",
        "frequency": "WEDNESDAY",
        "completed": False,
        "timeFrame": ("2:00PM", "3:00PM")
    }

    Item6 = {
        "item_type": "FREQUENT",
        "title": "Water the Plants",
        "content": "Water all the indoor plants.",
        "frequency": "WEDNESDAY",
        "completed": False,
        "timeFrame": ("8:00AM", "8:30AM")
    }

    Item7 = {
        "item_type": "FREQUENT",
        "title": "Gym Session",
        "content": "Workout at the gym after work.",
        "frequency": "THURSDAY",
        "completed": False,
        "timeFrame": ("5:00PM", "6:30PM")
    }

    Item8 = {
        "item_type": "FREQUENT",
        "title": "Read a Book",
        "content": "Read a chapter from a book.",
        "frequency": "THURSDAY",
        "completed": False,
        "timeFrame": ("8:00PM", "9:00PM")
    }

    Item9 = {
        "item_type": "FREQUENT",
        "title": "Office Cleanup",
        "content": "Organize and clean the office space.",
        "frequency": "FRIDAY",
        "completed": False,
        "timeFrame": ("3:00PM", "4:00PM")
    }

    Item10 = {
        "item_type": "FREQUENT",
        "title": "Evening Workout",
        "content": "Workout at the gym after work.",
        "frequency": "FRIDAY",
        "completed": False,
        "timeFrame": ("5:00PM", "6:30PM")
    }

    Item11 = {
        "item_type": "FREQUENT",
        "title": "Family Time",
        "content": "Spend quality time with the family.",
        "frequency": "SATURDAY",
        "completed": False,
        "timeFrame": ("2:00PM", "4:00PM")
    }

    Item12 = {
        "item_type": "FREQUENT",
        "title": "Grocery Shopping",
        "content": "Restock essential items for the week.",
        "frequency": "SATURDAY",
        "completed": False,
        "timeFrame": ("10:00AM", "11:00AM")
    }

    Item13 = {
        "item_type": "FREQUENT",
        "title": "Meal Prep",
        "content": "Prepare meals for the upcoming week.",
        "frequency": "SUNDAY",
        "completed": False,
        "timeFrame": ("11:00AM", "1:00PM")
    }

    Item14 = {
        "item_type": "FREQUENT",
        "title": "Relaxation Time",
        "content": "Take some time to relax and recharge.",
        "frequency": "SUNDAY",
        "completed": False,
        "timeFrame": ("5:00PM", "7:00PM")
    }

    Item15 = {
        "item_type": "FREQUENT",
        "title": "Eat a carrot",
        "content": "Eat about 2 of them",
        "frequency": "EVERYDAY",
        "completed": False,
        "timeFrame": ("1:00AM", "2:00AM")
    }


    SampleTodo = {
        "item_type": "TODO",
        "title": "eat food",
        "content": "eat food",
        "completed": False,
    }

    table = dynamodb.Table(AWS_DYNAMODB_TABLE_NAME)
    table.put_item(Item=Item1)
    table.put_item(Item=Item2)
    table.put_item(Item=Item3)
    table.put_item(Item=Item4)
    table.put_item(Item=Item5)
    table.put_item(Item=Item6)
    table.put_item(Item=Item7)
    table.put_item(Item=Item8)
    table.put_item(Item=Item9)
    table.put_item(Item=Item10)
    table.put_item(Item=Item11)
    table.put_item(Item=Item12)
    table.put_item(Item=Item13)
    table.put_item(Item=Item14)
    table.put_item(Item=SampleTodo)

    

    User1 = {
        'username': 'test',
        'attribute_type': "login",
    }
    table = dynamodb.Table(AWS_DYNAMODB_TABLE_NAME2)
    table.put_item(Item=User1)


# delete_table()
# create_dynamodb_table()
# addDummyData()
# show()

# Initialize the parser
parser = argparse.ArgumentParser(description="Manipulating the table")

# Define the arguments
parser.add_argument('-d', action='store_true', help="Deletes Table")
parser.add_argument('-c', action='store_true', help="Creates Table")
parser.add_argument('-a', action='store_true', help="Add dummy values")
parser.add_argument('-s', action='store_true', help="Show Table")
parser.add_argument('-A', action='store_true', help="Reset Table, add dummy data, and display table")

# Parse the arguments
args = parser.parse_args()

# Debugging output to check if args are parsed
print(args)

# Conditional checks for the flags
if args.d:
    delete_table()

if args.c:
    create_dynamodb_table()

if args.a:
    addDummyData()

if args.s:
    show()

if args.A:
    delete_table()
    create_dynamodb_table()
    addDummyData()
    show()







