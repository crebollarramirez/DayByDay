import os
import time
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import csv

load_dotenv()

class DynamoDB_Manager:
    """
    A class to manage a DynamoDB table, including creating, deleting, and clearing the table,
    as well as adding dummy data and retrieving items.
    """
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

    @classmethod
    def delete_table(cls) -> None:
        """
        Deletes the DynamoDB table specified in the environment variables.
        Waits until the table is completely deleted.
        """
        # Delete the table
        cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).delete()
        print(f"Deleting table {cls.__AWS_DYNAMODB_TABLE_NAME}...")

        while True:
            try:
                cls.__DYNAMODB.Table(
                    cls.__AWS_DYNAMODB_TABLE_NAME
                ).wait_until_not_exists()
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
    def clear_table(cls) -> None:
        """
        Clears all items from the DynamoDB table without deleting the table itself.
        """
        # Scan the table to get all items
        scan_response = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).scan()
        items = scan_response.get("Items", [])

        # Loop through the items and delete each one
        with cls.__DYNAMODB.Table(
            cls.__AWS_DYNAMODB_TABLE_NAME
        ).batch_writer() as batch:
            for item in items:
            # Assuming your table has 'user_id' as hash key and 'item_id' as range key
                batch.delete_item(
                    Key={
                    "user_id": item["user_id"],
                    "item_id": item["item_id"],
                    }
                )

        print(
            f"All items in table {cls.__AWS_DYNAMODB_TABLE_NAME} cleared successfully."
        )

    @classmethod
    def create_dynamodb_table(cls) -> None:
        """
        Creates a DynamoDB table with the specified schema and global secondary index.
        """
        # Define the table
        table_name = cls.__AWS_DYNAMODB_TABLE_NAME

        try:
            # Create the DynamoDB table
            table = cls.__DYNAMODB.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "user_id", "KeyType": "HASH"},  # Partition Key
                    {"AttributeName": "item_id", "KeyType": "RANGE"},  # Sort Key
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "user_id",
                        "AttributeType": "S",
                    },  # Primary Partition Key
                    {
                        "AttributeName": "item_id",
                        "AttributeType": "S",
                    },  # Primary Sort Key
                    {
                        "AttributeName": "item_type",
                        "AttributeType": "S",
                    },  # Attribute for GSI
                ],
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "ItemTypeIndex",  # GSI Name
                        "KeySchema": [
                            {
                                "AttributeName": "user_id",
                                "KeyType": "HASH",
                            },
                            {
                                "AttributeName": "item_type",
                                "KeyType": "RANGE",
                            },  # GSI Sort Key
                        ],
                        "Projection": {
                            "ProjectionType": "ALL"
                        },  # Store all attributes in GSI
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 5,
                            "WriteCapacityUnits": 5,
                        },
                    }
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )

            # Wait until the table is created
            print(f"Table {table_name} created successfully.")

        except ClientError as e:
            print(f'Error creating table: {e.response["Error"]["Message"]}')

    @classmethod
    def get_all_items(cls) -> tuple[dict, int]:
        """
        Retrieves all items from the DynamoDB table, grouped by date and sorted by content.
        
        Returns:
            tuple: A dictionary where keys are dates and values are lists of items (sorted by content),
               and the total number of items.
        """
        items = {}
        total_items = 0

        # Scan the table to get all items
        scan_response = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).scan()
        for item in scan_response.get("Items", []):
            date = item.get("date")
            if date not in items:
                items[date] = []
            items[date].append(item)
            total_items += 1

        # Sort the items by content
        for date in items:
            items[date].sort(key=lambda x: x.get("content", ""))

        return items, total_items

    @classmethod
    def scan_table(cls) -> list:
        """
        Scans the DynamoDB table and retrieves all items.
        
        Returns:
            list: A list of all items in the table.
        """
        items = []

        response = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).scan()

        while True:
            items.extend(response.get("Items", []))

            # Check if there are more items to fetch
            if "LastEvaluatedKey" in response:
                response = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME).scan(
                    ExclusiveStartKey=response["LastEvaluatedKey"]
                )
            else:
                break

        return items

    @classmethod
    def show(cls) -> None:
        """
        Lists all DynamoDB tables and prints all items in each table.
        """
        # List DynamoDB tables
        tables = (
            cls.__DYNAMODB.tables.all()
        )  # Change to use the resource for listing tables
        print("Tables:", [table.name for table in tables])  # Print names of the tables

        # Print all items in each table
        for table in tables:
            print(f"\nTable: {table.name}")
            items = cls.scan_table()  # Now this function is defined before being called

            # Print each item and its attributes
            for item in items:
                print(item)

    @classmethod
    def addDummyData(cls) -> None:
        """
        Adds dummy data to the DynamoDB table from a CSV file.
        """
        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)

        # Getting test data from csv file
        items = []
        file_path = os.path.join(parentDir, "test_data", "todos_test_data.csv")
        with open(file_path, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert the completed field to a boolean
                row["completed"] = row["completed"] == "True"
                items.append(row)

        # Adding items to the table
        table = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME)
        for item in items:
            try:
                table.put_item(Item=item)
            except ClientError as e:
                print(f'Error adding item: {e.response["Error"]["Message"]}')

        print(f"Total items added: {len(items)}")  # Debugging statement