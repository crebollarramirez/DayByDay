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




if __name__ == "__main__":
    table_name = create_dynamodb_table()
    add_sample_item(table_name)
