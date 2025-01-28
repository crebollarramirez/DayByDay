import os
import time
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import csv
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
                    {"AttributeName": "item_id", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "user#item_type", "AttributeType": "S"},  # String type
                    {"AttributeName": "item_id", "AttributeType": "S"},  # String type
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
        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)
        
        items = []
        with open(parentDir + "/test_data/tasks_test_data.csv", mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert the completed field to a boolean
                row["completed"] = row["completed"] == "True"
                row["timeFrame"] = tuple(row["timeFrame"].replace("[", "").replace("]", "").split(","))
                items.append(row)



        # item1 = {
        #     "user#item_type": "chris#TASK",
        #     "user#item_id": "chris#a1",  # Replace with a unique ID as needed
        #     "title": "Math Homework",
        #     "content": "Complete Chapter 5 exercises.",
        #     "completed": False,
        #     "timeFrame": ("14:00", "16:00"),
        #     "date": "10-21-2024"
        # }

        # item2 = {
        #     "user#item_type": "chris#TASK",
        #     "user#item_id": "chris#a2",  # Replace with a unique ID as needed
        #     "title": "Grocery Shopping",
        #     "content": "Buy vegetables, fruits, and bread.",
        #     "completed": False,
        #     "timeFrame": ("10:00", "11:00"),
        #     "date": "10-22-2024"
        # }

        # item3 = {
        #     "user#item_type": "chris#TASK",
        #     "user#item_id": "chris#a3",  # Replace with a unique ID as needed
        #     "title": "Team Meeting",
        #     "content": "Discuss project progress with team.",
        #     "completed": True,
        #     "timeFrame": ("09:00", "10:30"),
        #     "date": "10-23-2024"
        # }

        # item4 = {
        #     "user#item_type": "chris#TASK",
        #     "user#item_id": "chris#a4",  # Replace with a unique ID as needed
        #     "title": "Workout",
        #     "content": "Upper body strength training.",
        #     "completed": False,
        #     "timeFrame": ("07:00", "08:00"),
        #     "date": "10-24-2024"
        # }

        # item5 = {
        #     "user#item_type": "chris#TASK",
        #     "user#item_id": "chris#a5",  # Replace with a unique ID as needed
        #     "title": "Client Presentation",
        #     "content": "Present the marketing plan to the client.",
        #     "completed": False,
        #     "timeFrame": ("13:00", "14:30"),
        #     "date": "10-25-2024"
        # }
        
        table = cls.__DYNAMODB.Table(cls.__AWS_DYNAMODB_TABLE_NAME)
        for item in items:
            table.put_item(Item=item)
            # print(item)
        # table.put_item(Item=item2)
        # table.put_item(Item=item3)
        # table.put_item(Item=item4)
        # table.put_item(Item=item5)