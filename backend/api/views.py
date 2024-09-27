from django.http import JsonResponse
from boto3.dynamodb.conditions import Attr
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_todo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')

        print(data)
        table = get_tasks_table()
        response = table.put_item(
            Item={
                'item_type': "TODO",
                'title': content,
                'content': content
            }
        )

        return JsonResponse({'message': 'Task created', 'data': data}, status=201)

@csrf_exempt
def delete_todo(request, title, item_type):
    if request.method == 'DELETE':
        table = get_tasks_table()
        print("we are deleting")
        print(f"content: {title}".format(title))
        # Delete the task from the table by its taskId
        print(title + '\n\n\n')
        table.delete_item(
            Key={
                'title': title,
                'item_type': item_type
            }
        )
        
        return JsonResponse({'message': 'Task deleted successfully.'}, status=204)


def list_todo(request):
    if request.method == 'GET':
        table = get_tasks_table()
        
        # Scan the table and filter for items with item_type = 'todo'
        response = table.scan(
            FilterExpression=Attr('item_type').eq('TODO')
        )
        
        return JsonResponse(response['Items'], safe=False)
    
@csrf_exempt
def edit_todo(request, title):
    if request.method == 'PUT':
        table = get_tasks_table()

        data = json.loads(request.body)
        newData = data.get('newData')
        print(newData)

        response = table.update_item(
        Key={
            'title': title,

        },
        UpdateExpression = "set content = :c",
        ExpressionAttributeValues={
            ':c' : newData
        },
        ReturnValues="UPDATED_NEW"
        )
       
        return JsonResponse({'message': 'Task updated successfully', 'updated': response['Attributes']}, status=200)
   
    return JsonResponse({'error': 'Invalid request method'}, status=405)
