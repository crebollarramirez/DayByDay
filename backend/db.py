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
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
    endpoint_url="http://localhost:8080",  # For local DynamoDB instance
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
                {"AttributeName": "id#item_type", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "id#title", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "id#item_type", "AttributeType": "S"},  # String type
                {"AttributeName": "id#title", "AttributeType": "S"},  # String type
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        # Wait until the table is created
        print(f"Table {table_name} created successfully.")

    except ClientError as e:
        print(f'Error creating table: {e.response["Error"]["Message"]}')

    return table_name


def scan_table(table_name):
    items = []
    table = dynamodb.Table(table_name)  # Use the resource object here

    response = table.scan()

    while True:
        items.extend(response.get("Items", []))

        # Check if there are more items to fetch
        if "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        else:
            break

    return items


def show():
    # List DynamoDB tables
    tables = dynamodb.tables.all()  # Change to use the resource for listing tables
    print("Tables:", [table.name for table in tables])  # Print names of the tables

    # Print all items in each table
    for table in tables:
        print(f"\nTable: {table.name}")
        items = scan_table(
            table.name
        )  # Now this function is defined before being called

        # Print each item and its attributes
        for item in items:
            print(item)
            print()


def addDummyData():
    Item1 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Morning Walk",
        "content": "Take the dog for a morning walk.",
        "frequency": "MONDAY",
        "completed": False,
        "timeFrame": ("07:00", "08:00"),
    }

    Item2 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Team Check-In",
        "content": "Have a quick check-in with the team.",
        "frequency": "MONDAY",
        "completed": False,
        "timeFrame": ("11:00", "11:30"),
    }

    Item3 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Grocery Shopping",
        "content": "Buy groceries for the week.",
        "frequency": "TUESDAY",
        "completed": False,
        "timeFrame": ("10:00", "11:00"),
    }

    Item4 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Yoga Class",
        "content": "Attend a virtual yoga class.",
        "frequency": "TUESDAY",
        "completed": False,
        "timeFrame": ("18:00", "19:00"),
    }

    Item5 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Weekly Meeting",
        "content": "Attend the project weekly meeting.",
        "frequency": "WEDNESDAY",
        "completed": False,
        "timeFrame": ("14:00", "15:00"),
    }

    Item6 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Water the Plants",
        "content": "Water all the indoor plants.",
        "frequency": "WEDNESDAY",
        "completed": False,
        "timeFrame": ("08:00", "08:30"),
    }

    Item7 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Gym Session",
        "content": "Workout at the gym after work.",
        "frequency": "THURSDAY",
        "completed": False,
        "timeFrame": ("17:00", "20:00"),
    }

    Item8 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Read a Book",
        "content": "Read a chapter from a book.",
        "frequency": "THURSDAY",
        "completed": False,
        "timeFrame": ("20:00", "21:00"),
    }

    Item9 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Office Cleanup",
        "content": "Organize and clean the office space.",
        "frequency": "FRIDAY",
        "completed": False,
        "timeFrame": ("15:00", "16:00"),
    }

    Item10 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Evening Workout",
        "content": "Workout at the gym after work.",
        "frequency": "FRIDAY",
        "completed": False,
        "timeFrame": ("17:00", "18:30"),
    }

    Item11 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Family Time",
        "content": "Spend quality time with the family.",
        "frequency": "SATURDAY",
        "completed": False,
        "timeFrame": ("14:00", "16:00"),
    }

    Item12 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Grocery Shopping",
        "content": "Restock essential items for the week.",
        "frequency": "SATURDAY",
        "completed": False,
        "timeFrame": ("10:00", "11:00"),
    }

    Item13 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Meal Prep",
        "content": "Prepare meals for the upcoming week.",
        "frequency": "SUNDAY",
        "completed": False,
        "timeFrame": ("11:00", "13:00"),
    }

    Item14 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Relaxation Time",
        "content": "Take some time to relax and recharge.",
        "frequency": "SUNDAY",
        "completed": False,
        "timeFrame": ("17:00", "19:00"),
    }

    Item15 = {
        "id#item_type": "chris#FREQUENT",
        "id#title": "chris#Eat a carrot",
        "content": "Eat about 2 of them",
        "frequency": "EVERYDAY",
        "completed": False,
        "timeFrame": ("01:00", "02:00"),
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
    table.put_item(Item=Item15)


# Initialize the parser
parser = argparse.ArgumentParser(description="Manipulating the table")

# Define the arguments
parser.add_argument("-d", action="store_true", help="Deletes Table")
parser.add_argument("-c", action="store_true", help="Creates Table")
parser.add_argument("-a", action="store_true", help="Add dummy values")
parser.add_argument("-s", action="store_true", help="Show Table")
parser.add_argument(
    "-A", action="store_true", help="Reset Table, add dummy data, and display table"
)

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
