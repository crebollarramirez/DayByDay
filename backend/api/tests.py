from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient
from .models import Todo
from rest_framework_simplejwt.tokens import AccessToken
import uuid
import random
import csv
import os
import json


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.register_url = "/api/user/register/"  # Example URL, adjust as needed
        self.user_data = {
            "username": "testuser_1",  # Use a unique username for the setup
            "password": "testpassword",
        }
        # Register a new user in setup
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Obtain token for the registered user
        response = self.client.post(
            "/api/token/",
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.token = response.data.get(
            "access"
        )  # Adjust depending on your token structure
        self.assertIsNotNone(self.token, "Token was not generated")
    
    def test_user_registration_and_token(self):
        """Test user registration and token retrieval."""
        unique_username = "testuser_2"  # Unique username
        user_data = {
            "username": unique_username,
            "password": "testpassword",
        }

        response = self.client.post(self.register_url, user_data)

        # Print response data for debugging if the registration fails
        if response.status_code != status.HTTP_201_CREATED:
            print("User registration failed:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Obtain token for the registered user
        token_data = {"username": unique_username, "password": "testpassword"}
        response = self.client.post("/api/token/", token_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if token is returned in response
        self.assertIn("access", response.data)

    def test_authenticated_access(self):
        """Test authenticated access with the user's token."""
        response = self.client.get(
            "/api/todos/", HTTP_AUTHORIZATION="Bearer " + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodoListTests(APITestCase):
    def setUp(self):
        # Create a user with username 'chris' and password 'chris'
        self.user = User.objects.create_user(username="chris", password="chris")
        self.client = APIClient()

        # Generate a JWT token for the user
        self.token = AccessToken.for_user(self.user)
        # Set the token in the Authorization header for API requests
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_adding_todos(self):
        url = reverse("todos")
        response = self.client.get(url)
        todos = []

        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)

        with open(parentDir + "/test_data/todos_test_data.csv", mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert the completed field to a boolean
                row['completed'] = row['completed'] == 'True'
                todos.append(row)
        # Sending todo in the post request
        for todo in todos:
            response = self.client.post(url, data=todo)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url) 
        responseTodoList = response.data

        todosSorted = sorted(todos, key=lambda d: d['content']) # Sort by 'content'
        responseTodosSorted = sorted(responseTodoList, key=lambda d: d['content'])  # Sort API response by 'content'

        for expected, actual in zip(todosSorted, responseTodosSorted):
            self.assertTrue(str(expected['content']) == str(actual['content']))
                
    def test_delete_todos(self):
        url = reverse("todos")
        response = self.client.get(url)
        expected = response.data
        deletedItems = []

        # Getting random 250 items to delete
        for _ in range(1,250):
            randIndex = random.randint(0, len(expected)-1)
            deletedItems.append(expected[randIndex])
            del expected[randIndex]
        
        # Deleting 250 items from user data
        for itemToDelete in deletedItems:
            delete_url = reverse("delete-todo", kwargs={'item_id': itemToDelete['item_id'], 'item_type': itemToDelete['item_type']})
            response = self.client.delete(delete_url)
        
        # Getting the new list of todos - deleted data
        response = self.client.get(url)

        # sorting the lists to compare them.
        expectedList = sorted(expected, key=lambda d: d['content']) # Sort by 'content'
        actualList = sorted(response.data, key=lambda d: d['content']) # Sort by 'content'
        
        # Seeing if they are the same size:
        self.assertTrue(len(expectedList), len(actualList))
        
        # Checking if expected == actual
        for item1, item2 in zip(expectedList, actualList):
            self.assertTrue(str(item1['content']) == str(item2['content']))
        
    def test_complete_todo(self):
        todosURL = reverse("todos")
        response = self.client.get(todosURL)
        expected = response.data

        changedItems = []
        for _  in range(1,250):
            randomIndex = random.randint(0, len(expected)-1)
            expected[randomIndex]['completed'] = True if expected[randomIndex]['completed'] == "True" else False
            expected[randomIndex]['completed'] = not(expected[randomIndex]['completed'])
            changedItems.append(expected[randomIndex])

        for item in changedItems:
            data = {
                'completed': item['completed']
            }
            changeStatusURL = reverse("change-status", kwargs={'item_id': item['item_id'], 'item_type': item['item_type']})
            response = self.client.put(changeStatusURL, json.dumps(data), content_type='application/json')
        
        
        response = self.client.get(todosURL)
        actual = response.data

        expectedList = sorted(expected, key=lambda d: d['content']) # Sort by 'content'
        actualList = sorted(actual, key=lambda d: d['content']) # Sort by 'content'
        
        for item1, item2 in zip(expectedList, actualList):
            status1 = True if item1['completed'] == "True" else False
            status2 = True if item2['completed'] == "True" else False
            self.assertEqual(
                status1, status2
            )
    
    # def test_edit_todo(self):   
    #     todosURL = reverse("todos")
    #     response = self.client.get(todosURL)
    #     expected = response.data

    #     editedItems = []
    #     for _  in range(1,250):
    #         randomIndex = random.randint(0, len(expected)-1)
    #         expected[randomIndex]['content'] = "edit" + str(randomIndex)
    #         expected[randomIndex]['completed'] = True if expected[randomIndex]['completed'] == "True" else False
    #         expected[randomIndex]['completed'] = True if randomIndex % 2 == 0 else False
    #         editedItems.append(expected[randomIndex]) 

    #     for item in editedItems:
    #         data = {
    #             'completed': item['completed'],
    #             'content': item['content']
    #         }
    #         editURL = reverse("todos", kwargs={'item_id': item['item_id'], 'item_type': item['item_type']})
    #         response = self.client.put(editURL, json.dumps(data), content_type='application/json')

    #     response = self.client.get(todosURL)
    #     actual = response.data
        
    #     expectedList = sorted(expected, key=lambda d: d['content']) # Sort by 'content'
    #     actualList = sorted(actual, key=lambda d: d['content']) # Sort by 'content'
    #     print(len(expectedList))
    #     print(len(actualList))
    #     # for item1, item2 in zip(expectedList, actualList):
    #     #     status1 = True if item1['completed'] == "True" else False
    #     #     status2 = True if item2['completed'] == "True" else False
    #     #     # self.assertEqual(
    #     #     #     status1, status2
    #     #     # )
    #     #     # self.assertEqual(
    #     #     #     str(item1['content']), str(item2['content'])
    #     #     # )