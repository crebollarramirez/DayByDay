import os
import time
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
load_dotenv()


class DynamoDB_Manager:
    __AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    __AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
    __AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    __AWS_DYNAMODB_TABLE_NAME = os.getenv("AWS_DYNAMODB_TABLE_NAME")
    __ENDPOINT_URL = os.getenv("ENDPOINT_URL")

    __DYNAMODB = boto3.resource(
    "dynamodb",
    aws_access_key_id=__AWS_ACCESS_KEY_ID,
    aws_secret_access_key=__AWS_SECRET_ACCESS_KEY,
    region_name=__AWS_REGION_NAME,
    endpoint_url=__ENDPOINT_URL,  # For local DynamoDB instance
    )    
    def __init__():
        pass

    @classmethod
    def delete_table(cls):
        # Delete the table
        cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).delete()
        print(f"Deleting table {cls.__AWS_DYNAMODB_TABLE_NAME}...")

        # Wait until the table is delete

        while True:
            try:
                cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).wait_until_not_exists()
                print(f"Table {cls.__AWS_DYNAMODB_TABLE_NAME} deleted successfully.")
                break
            except Exception as e:
                print("Waiting for table to delete...")
                time.sleep(5)

        print("Tables Deleted.")

    """
    Clears all items from a DynamoDB table without deleting the table itself.
    """
    @classmethod
    def clear_table(cls):
        # Scan the table to get all items
        scan_response = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).scan()
        items = scan_response.get("Items", [])
        
        # Loop through the items and delete each one
        with cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).batch_writer() as batch:
            for item in items:
                # Assuming your table has 'user#item_type' as hash key and 'user#item_id' as range key
                batch.delete_item(
                    Key={
                        "user#item_type": item["user#item_type"],
                        "user#item_id": item["user#item_id"]
                    }
                )
        
        print(f"All items in table {cls.__AWS_DYNAMODB_TABLE_NAME} cleared successfully.")
    
    @classmethod
    def create_dynamodb_table(cls):
        # Define the table
        table_name = cls.__AWS_DYNAMODB_TABLE_NAME

        try:
            # Create the DynamoDB table
            table = cls.__DYNAMODB.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "user#item_type", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "user#item_id", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "user#item_type", "AttributeType": "S"},  # String type
                    {"AttributeName": "user#item_id", "AttributeType": "S"},  # String type
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )

            # Wait until the table is created
            print(f"Table {table_name} created successfully.")

        except ClientError as e:
            print(f'Error creating table: {e.response["Error"]["Message"]}')

    @classmethod
    def scan_table(cls):
        items = []

        response = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).scan()

        while True:
            items.extend(response.get("Items", []))

            # Check if there are more items to fetch
            if "LastEvaluatedKey" in response:
                response = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            else:
                break

        return items

    @classmethod
    def show(cls):
        # List DynamoDB tables
        tables = cls.__DYNAMODB.tables.all()  # Change to use the resource for listing tables
        print("Tables:", [table.name for table in tables])  # Print names of the tables

        # Print all items in each table
        for table in tables:
            print(f"\nTable: {table.name}")
            items = cls.scan_table()  # Now this function is defined before being called

            # Print each item and its attributes
            for item in items:
                print(item)
                print()

    @classmethod
    def addDummyData(cls):
        Item1 = {
            "user#item_type": "chris#TODO",
            "user#item_id": "chris#asdfsd77Faddsf",
            "content": "Take the dog for a morning walk.",
            "completed": False,
        }
        Item2 = {
            "user#item_type": "testuser#TODO",
            "user#item_id": "testuser#asdfsd77Faddsf",
            "content": "Take the dog outside.",
            "completed": False,
        }
        Item3 = {
            "user#item_type": "testuser_1#TODO",
            "user#item_id": "testuser_1#asdfsd77Faddsf",
            "content": "Take the dog outside.",
            "completed": False,
        }
        Item4 = {
            "user#item_type": "testuser_2#TODO",
            "user#item_id": "testuser_2#asdfsd77Faddsf",
            "content": "Take the dog outside.",
            "completed": False,
        }
        table = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME)
        table.put_item(Item=Item1)
        table.put_item(Item=Item2)
        table.put_item(Item=Item3)
        table.put_item(Item=Item4)


