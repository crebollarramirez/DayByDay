from django.http import JsonResponse
from .dynamodb import get_tasks_table
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        print(data)
        table = get_tasks_table()
        response = table.put_item(
            Item={
                'content': content
            }
        )

        return JsonResponse({'message': 'Task created', 'data': data}, status=201)

@csrf_exempt
def delete_task(request, content):
    if request.method == 'DELETE':
        table = get_tasks_table()
        print("we are deleting")
        print(f"content: {content}".format(content))
        # Delete the task from the table by its taskId
        table.delete_item(
            Key={
                'content': content
            }
        )
        
        return JsonResponse({'message': 'Task deleted successfully.'}, status=204)


def list_tasks(request):
    if request.method == 'GET':
        table = get_tasks_table()
        response = table.scan()
        return JsonResponse(response['Items'], safe=False)
    
@csrf_exempt
def clear_tasks(request):
    if request.method == 'DELETE':  # Use DELETE method for clearing tasks
        table = get_tasks_table()
        
        # Scan the table to get all items
        response = table.scan()
        items = response['Items']
        
        # Loop through the items and delete each one
        for item in items:
            # Assuming 'taskId' is the primary key of the items
            table.delete_item(
                Key={
                    'content': item['content']  # Replace 'taskId' with your actual primary key name
                }
            )
        
        return JsonResponse({'message': 'All tasks have been deleted.'}, status=204)

