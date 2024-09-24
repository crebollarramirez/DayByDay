import boto3
from django.conf import settings

def get_dynamodb_resource():
    return boto3.resource(
        'dynamodb',
        region_name=settings.AWS_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

def get_tasks_table():
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(settings.AWS_DYNAMODB_TABLE_NAME)