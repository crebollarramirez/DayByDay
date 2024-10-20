from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from .Dynamo import DynamoDB_Manager
import random
import csv
import os
import json

"""
Test case for user authentication processes including registration, 
token generation, and access to authenticated endpoints.
"""


class AuthenticationTestCase(TestCase):
    """
    Test case for user authentication processes including registration,
    token generation, and access to authenticated endpoints.
    """

    def setUp(self) -> None:
        self.register_url = "/api/user/register/"
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

        """
        Test the user registration process and token retrieval.
        - Verifies that a user can be registered successfully.
        - Ensures the token endpoint returns a valid access token after registration.
        """

    def test_user_registration_and_token(self) -> None:
        """Test user registration and token retrieval."""
        unique_username = "testuser_2"  # Unique username
        user_data = {
            "username": unique_username,
            "password": "testpassword",
        }

        # Post request to register the new user
        response = self.client.post(self.register_url, user_data)

        # Print response data for debugging if the registration fails
        if response.status_code != status.HTTP_201_CREATED:
            print("User registration failed:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt to retrieve a token for the newly registered user
        token_data = {"username": unique_username, "password": "testpassword"}
        response = self.client.post("/api/token/", token_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains an access token
        self.assertIn("access", response.data)

    """
    Test access to a protected API endpoint using a valid token.
    - Confirms that the user can access the `todos` endpoint when authenticated.
    """

    def test_authenticated_access(self) -> None:
        # Send a GET request to the protected todos endpoint with the user's token
        response = self.client.get(
            "/api/todos/", HTTP_AUTHORIZATION="Bearer " + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TasksListTests(APITestCase):
    def setUp(self) -> None:
        # Create a user with username 'chris' and password 'chris'
        self.user = User.objects.create_user(username="chris", password="chris")
        self.client = APIClient()

        # Generate a JWT token for the user
        self.token = AccessToken.for_user(self.user)
        # Set the token in the Authorization header for API requests
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)

        self.DATE = "10-20-2024"
        self.tasksTestData = []
        with open(parentDir + "/test_data/tasks_test_data.csv", mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert the completed field to a boolean
                row["completed"] = row["completed"] == "True"
                row["timeFrame"] = row["timeFrame"].replace("[", "").replace("]", "").split(",")
                row['user'], row['item_id'] = row['user#item_id'].split("#")
                _, row['item_type'] = row['user#item_type'].split("#")
                self.tasksTestData.append(row)

    # If this works well, we can rely one creating new data for each test
    def test_01_get_week(self) -> None:
        getTasksURL = reverse("week-list", kwargs={'date': self.DATE})
        response = self.client.get(getTasksURL)
        actual = []
        for value in response.data.values():
            for item in value.values():
                actual.append(item)

        expectedSorted = sorted(
            self.tasksTestData, key=lambda d: (d["title"] + d["content"])
        )
        actualSorted = sorted(actual, key=lambda d: (d["title"] + d["content"]))


        self.assertEqual(len(actual), len(self.tasksTestData))
        for item1, item2 in zip(actualSorted, expectedSorted):
            self.assertEqual(str(item1["title"]), str(item2["title"]))
            self.assertEqual(str(item1["content"]), str(item2["content"]))
            self.assertEqual(item1["timeFrame"][0], item2["timeFrame"][0])
            self.assertEqual(item1["timeFrame"][1], item2["timeFrame"][1])
            self.assertEqual(item1["completed"] == True, item2["completed"] == True)
            self.assertEqual(str(item1["date"]), str(item2["date"]))
            self.assertEqual(str(item1["item_id"]), str(item2["item_id"]))

    # def test_02_create_task(self) -> None:
    #     tasksToAdd = [
    #         {
    #             "title": "This is a test",
    #             "content": "this is for testing purposes",
    #             "timeFrame": ['10:00', '13:00'],
    #             "date": "10-24-2024",
    #             "item_type": "TASK",
    #             "completed": False,
    #         },
    #         {
    #             "title": "Another new Task",
    #             "content": "This is for testing purposes",
    #             "item_type": "TASK",
    #             "completed": False,
    #             "timeFrame": ['8:00', '10:00'],
    #             "date": "10-21-2024",
    #         }
    #     ]

    #     self.tasksTestData += tasksToAdd

    #     for task in tasksToAdd:
    #         createTaskURL = reverse("tasks")
    #         response = self.client.post(
    #             createTaskURL, data=task, 
    #         )
    #         print("this is the response")
    #         print(response)
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Now getting the week date using GET request
    #     getWeekURL = reverse("tasks")
    #     response = self.client.get(getWeekURL, format='json')

    #     actual = []
    #     for value in response.data.values():
    #         for item in value.values():
    #             actual.append(item)
    #     actualSorted = sorted(actual, key=lambda d: (d["title"] + d["content"]))
    #     expectedSorted = sorted(self.tasksTestData, key=lambda d: (d["title"] + d["content"]))

    #     self.assertEqual(len(actual), len(self.tasksTestData))
    #     for item1, item2 in zip(actualSorted, expectedSorted):
    #         self.assertEqual(str(item1["title"]), str(item2["title"]))
    #         self.assertEqual(str(item1["content"]), str(item2["content"]))
    #         self.assertEqual(str(item1["timeFrame"]), str(item2["timeFrame"]))
    #         self.assertEqual(item1["completed"] == True, item2["completed"] == True)
    #         self.assertEqual(str(item1["date"]), str(item2["date"]))

    def test_03_complete_task(self) -> None:
        # Getting the week before any changes to the task
        getTasksURL = reverse("tasks")
        response = self.client.get(getTasksURL, format='json')

        expected = []
        for value in response.data.values():
            for item in value.values():
                expected.append(item)

        # Editing Random items in the expected
        changedItems = []
        for _ in range(len(expected)):
            randomIndex = random.randint(0, len(expected) - 1)
            expected[randomIndex]['completed'] = not("True" == expected[randomIndex]['completed'])
            changedItems.append(expected[randomIndex])

        # Now attempting to edit those random items in actual tasks
        for item in changedItems:
            changeStatusURL = reverse(
                "change-status",
                kwargs={"item_id": item["item_id"], "item_type": item["item_type"]},
            )

            data = {
                    "completed": item["completed"],
                    }

            response = self.client.put(
                changeStatusURL, json.dumps(data), content_type="application/json"
            )

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Now getting data again with hopefully edited items
        tasksURL = reverse("tasks")
        response = self.client.get(tasksURL)
        
        actual = []
        for value in response.data.values():
            for item in value.values():
                actual.append(item)

        # Sorting the lists for comparing
        expectedList = sorted(expected, key=lambda d: (d["title"] + d["content"]))  # Sort by 'content'
        actualList = sorted(actual, key=lambda d: (d["title"] + d["content"]))  # Sort by 'content'

        # making sure the size didnt change
        self.assertEqual(len(actual), len(expected))

        # Comparing actual and expected
        for item1, item2 in zip(expectedList, actualList):
            self.assertEqual(str(item1["title"]), str(item2["title"]))
            self.assertEqual(str(item1["content"]), str(item2["content"]))
            self.assertEqual(str(item1["timeFrame"]), str(item2["timeFrame"]))
            self.assertEqual(item1["completed"] == True, item2["completed"] == True)
            self.assertEqual(str(item1["date"]), str(item2["date"]))


    def test_04_update_task(self) -> None:
        pass
    
    def test_05_delete_task(self) -> None:
        # Getting the week before any changes to the task
        getTasksURL = reverse("tasks")
        response = self.client.get(getTasksURL)

        expected = []
        for value in response.data.values():
            for item in value.values():
                expected.append(item)

        # Editing Random items in the expected
        deletedItems = []
        for _ in range(2):
            randomIndex = random.randint(0, len(expected) - 1)
            deletedItems.append(expected[randomIndex])
            del expected[randomIndex]

        # Now attempting to edit those random items in actual tasks
        for item in deletedItems:
            deleteURL = reverse(
                "delete-task",
                kwargs={"item_id": item["item_id"], "item_type": item["item_type"]},
            )
            response = self.client.delete(
                deleteURL
            )

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Now getting data again with hopefully edited items
        tasksURL = reverse("tasks")
        response = self.client.get(tasksURL)
        
        actual = []
        for value in response.data.values():
            for item in value.values():
                actual.append(item)

        # Sorting the lists for comparing
        expectedList = sorted(expected, key=lambda d: (d["title"] + d["content"]))  # Sort by 'content'
        actualList = sorted(actual, key=lambda d: (d["title"] + d["content"]))  # Sort by 'content'

        # making sure the size didnt change
        self.assertEqual(len(actual), len(expected))

        # Comparing actual and expected
        for item1, item2 in zip(expectedList, actualList):
            self.assertEqual(str(item1["title"]), str(item2["title"]))
            self.assertEqual(str(item1["content"]), str(item2["content"]))
            self.assertEqual(str(item1["timeFrame"]), str(item2["timeFrame"]))
            self.assertEqual(item1["completed"] == True, item2["completed"] == True)
            self.assertEqual(str(item1["date"]), str(item2["date"]))

    def test_06_overlap_task_case(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        super(TasksListTests, cls).tearDownClass()
        DynamoDB_Manager.clear_table()


"""
Test suite for Todo-related operations in the API, including adding, deleting,
marking todos as complete, and editing todos. Each test ensures that the 
functionality performs correctly using Django's testing framework (APITestCase).
"""


class TodoListTests(APITestCase):
    """
    Sets up the test environment by creating a test user and obtaining a JWT token.
    The token is included in the Authorization header for authenticated API requests.
    """

    def setUp(self) -> None:
        # Create a user with username 'chris' and password 'chris'
        self.user = User.objects.create_user(username="chris", password="chris")
        self.client = APIClient()

        # Generate a JWT token for the user
        self.token = AccessToken.for_user(self.user)
        # Set the token in the Authorization header for API requests
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    """
    Tests adding todos to the system by reading a CSV file containing test data,
    sending POST requests for each todo, and verifying that the todos are successfully added.
    Validates that the number of todos returned matches the expected number
    and that their content is identical.
    """

    def test_01_create_todos(self) -> None:
        url = reverse("todos")
        response = self.client.get(url)
        todos = []

        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)

        with open(parentDir + "/test_data/todos_test_data.csv", mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert the completed field to a boolean
                row["completed"] = row["completed"] == "True"
                todos.append(row)
        # Sending todo in the post request
        for todo in todos:
            response = self.client.post(url, data=todo)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        responseTodoList = response.data

        todosSorted = sorted(todos, key=lambda d: d["content"])  # Sort by 'content'
        responseTodosSorted = sorted(
            responseTodoList, key=lambda d: d["content"]
        )  # Sort API response by 'content'

        # First checking if the length of actual == length of expected
        self.assertTrue(len(todosSorted), len(responseTodosSorted))

        # Seeing if all todos were added correctly
        for expected, actual in zip(todosSorted, responseTodosSorted):
            self.assertTrue(str(expected["content"]) == str(actual["content"]))

    """
    Tests deleting a subset of todos by randomly selecting 250 todos from the 
    current list, deleting them, and verifying that the correct todos were deleted.
    """

    def test_02_test_delete_todos(self) -> None:
        url = reverse("todos")
        response = self.client.get(url)
        expected = response.data
        deletedItems = []

        # Getting random 250 items to delete
        for _ in range(1, 250):
            randIndex = random.randint(0, len(expected) - 1)
            deletedItems.append(expected[randIndex])
            del expected[randIndex]

        # Deleting 250 items from user data
        for itemToDelete in deletedItems:
            delete_url = reverse(
                "delete-todo",
                kwargs={
                    "item_id": itemToDelete["item_id"],
                    "item_type": itemToDelete["item_type"],
                },
            )
            response = self.client.delete(delete_url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Getting the new list of todos - deleted data
        response = self.client.get(url)

        # sorting the lists to compare them.
        expectedList = sorted(expected, key=lambda d: d["content"])  # Sort by 'content'
        actualList = sorted(
            response.data, key=lambda d: d["content"]
        )  # Sort by 'content'

        # Seeing if they are the same size:
        self.assertTrue(len(expectedList), len(actualList))

        # Checking if expected == actual
        for item1, item2 in zip(expectedList, actualList):
            self.assertTrue(str(item1["content"]) == str(item2["content"]))

    """
    Tests toggling the completion status of a random subset of todos.
    The test retrieves 250 todos, flips their 'completed' status, and verifies
    the changes are accurately reflected in the database.
    """

    def test_03_test_complete_todo(self) -> None:
        todosURL = reverse("todos")
        response = self.client.get(todosURL)
        expected = response.data

        changedItems = []
        for _ in range(1, 250):
            randomIndex = random.randint(0, len(expected) - 1)
            expected[randomIndex]["completed"] = (
                True if expected[randomIndex]["completed"] == "True" else False
            )
            expected[randomIndex]["completed"] = not (
                expected[randomIndex]["completed"]
            )
            changedItems.append(expected[randomIndex])

        for item in changedItems:
            data = {"completed": item["completed"]}
            changeStatusURL = reverse(
                "change-status",
                kwargs={"item_id": item["item_id"], "item_type": item["item_type"]},
            )
            response = self.client.put(
                changeStatusURL, json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(todosURL)
        actual = response.data

        expectedList = sorted(expected, key=lambda d: d["content"])  # Sort by 'content'
        actualList = sorted(actual, key=lambda d: d["content"])  # Sort by 'content'

        for item1, item2 in zip(expectedList, actualList):
            status1 = True if item1["completed"] == "True" else False
            status2 = True if item2["completed"] == "True" else False
            self.assertEqual(status1, status2)

    """
    Tests editing the content and completion status of 250 randomly selected todos.
    The test ensures that the changes are successfully applied and verified.
    """

    def test_04_test_edit_todo(self) -> None:
        todosURL = reverse("todos")
        response = self.client.get(todosURL)
        expected = response.data

        editedItems = []
        for _ in range(0, 250):
            randomIndex = random.randint(0, len(expected) - 1)
            expected[randomIndex]["content"] = "edit" + str(randomIndex)
            expected[randomIndex]["completed"] = (
                True if expected[randomIndex]["completed"] == "True" else False
            )
            expected[randomIndex]["completed"] = True if randomIndex % 2 == 0 else False
            editedItems.append(expected[randomIndex])

        for item in editedItems:
            data = {"completed": item["completed"], "content": item["content"]}
            editURL = reverse(
                "edit-todo",
                kwargs={"item_id": item["item_id"], "item_type": item["item_type"]},
            )
            response = self.client.put(
                editURL, json.dumps(data), content_type="application/json"
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(todosURL)
        actual = response.data

        expectedList = sorted(expected, key=lambda d: d["item_id"])  # Sort by item_id
        actualList = sorted(actual, key=lambda d: d["item_id"])  # Sort by item_id

        # Before we check if expected == actual, lets make sure the size stays the same
        self.assertEqual(len(expectedList), len(actualList))

        # Now check if all expected is identical to actual
        for item1, item2 in zip(expectedList, actualList):
            status1 = True if item1["completed"] == "True" else False
            status2 = True if item2["completed"] == "True" else False

            # Checking if the item was actually updated
            self.assertEqual(status1, status2)
            self.assertEqual(str(item1["content"]), str(item2["content"]))
            if str(item1["content"]) != str(item2["content"]):
                print(str(item1["content"]))
                print(str(item2["content"]))

    """
    Clearing DynamoDB Database after testing
    """

    @classmethod
    def tearDownClass(cls) -> None:
        super(TodoListTests, cls).tearDownClass()
        DynamoDB_Manager.clear_table()
