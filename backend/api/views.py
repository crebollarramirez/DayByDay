from django.http import JsonResponse
from boto3.dynamodb.conditions import Attr
from django.views.decorators.csrf import csrf_exempt
import json

# nothing here for now