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

class AuthenticationTestCase(TestCase):
    """
    Test case for user authentication processes including registration, 
    token generation, and access to authenticated endpoints.
    """
    def setUp(self) -> None:
        """
        Set up the test environment.

        This method performs the following tasks:
        1. Sets the registration URL and user data for a new user.
        2. Registers a new user using the provided user data.
        3. Checks that the registration response status code is 201 (Created).
        4. Obtains a JWT token for the registered user.
        5. Checks that the token is successfully generated and not None.

        The setup ensures that a new user is registered and authenticated before each test.
        """
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

    def test_user_registration_and_token(self) -> None:
        """
        Test the user registration process and token retrieval.
        - Verifies that a user can be registered successfully.
        - Ensures the token endpoint returns a valid access token after registration.
        """
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


    def test_authenticated_access(self) -> None:
        """
        Test access to a protected API endpoint using a valid token.
        - Confirms that the user can access the `todos` endpoint when authenticated.
        """
        # Send a GET request to the protected todos endpoint with the user's token
        response = self.client.get(
            "/api/todos/?date=2025-01-01", HTTP_AUTHORIZATION="Bearer " + self.token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodosTests(APITestCase):
    """
    Sets up the test environment by creating a test user and obtaining a JWT token.
    The token is included in the Authorization header for authenticated API requests.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        This method performs the following tasks:
        1. Creates a user with username 'chris' and password 'chris'.
        2. Initializes the API client.
        3. Generates a JWT token for the user and sets it in the Authorization header for API requests.
        4. Clears the DynamoDB table and handles any exceptions that occur during this process.
        5. Reads dummy data from a CSV file and populates the todos dictionary with this data.
        6. Adds dummy data to the database.

        The todos dictionary is structured with dates as keys and lists of todo items as values.
        Each todo item is a dictionary with the fields from the CSV file, and the 'completed' field is converted to a boolean.
        """
        # Create a user with username 'chris' and password 'chris'
        self.user = User.objects.create_user(username="chris", password="chris")
        self.client = APIClient()

        # Generate a JWT token for the user
        self.token = AccessToken.for_user(self.user)
        # Set the token in the Authorization header for API requests
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        # Setting up the DynamoDB table and adding dummy data

        try:
            DynamoDB_Manager.clear_table()
        except Exception as e:
            print("There was an error clearing the table", e)

        currentDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(currentDir)
        self.expected_todos = {}
        self.expected_todos_count = 0  # Initialize the counter

        with open(parentDir + "/test_data/todos_test_data.csv", mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert the completed field to a boolean
                row["completed"] = row["completed"] == "True"
                date = row["date"]
                if date not in self.expected_todos:
                    self.expected_todos[date] = []
                self.expected_todos[date].append(row)
                self.expected_todos_count += 1  # Increment the counter

        # Sorting the todos by content
        for date in self.expected_todos.keys():
            self.expected_todos[date].sort(key=lambda d: d["content"])

        # Adding dummy data to database
        DynamoDB_Manager.addDummyData()

    def test_01_length_of_todos(self) -> None:
        """
        Test the length of todos for each date.

        This test performs the following tasks:
        1. Adds dummy data to the DynamoDB database.
        2. Retrieves todos from the API for each date in the todos dictionary.
        3. Compares the length of the retrieved todos with the length of the todos for each date.

        This test ensures that GET request does not change the size of the database, and retreieve the correct number of todos.
        """

        actual = {}
        for date in self.expected_todos.keys():
            url = reverse("todos") + f"?date={date}"
            actual[date] = self.client.get(url).data

        for date in self.expected_todos.keys():
            self.assertEqual(len(actual[date]), len(self.expected_todos[date]))

    def test_02_get_todos_of_date(self) -> None:
        """
        Test retrieving todos for a specific date.

        This test performs the following tasks:
        1. Adds dummy data to the DynamoDB database.
        2. Retrieves todos from the API for each date in the todos dictionary.
        3. Sorts the retrieved todos.
        4. Compares each field of the retrieved todos with the expected todos to ensure they match.

        The test ensures that the todos returned by the API for a specific date match the expected todos in the test data.
        """
        for date in self.expected_todos.keys():
            url = reverse("todos") + f"?date={date}"

            actual = sorted(
                self.client.get(url).data, key=lambda d: d["content"]
            )  # Sort by 'content'

            # Checking if we got the right todos for the date given
            for expected, actual in zip(actual, self.expected_todos[date]):
                self.assertEqual(str(expected["content"]), str(actual["content"]))
                self.assertEqual(str(expected["completed"]), str(actual["completed"]))
                self.assertEqual(str(expected["item_id"]), str(actual["item_id"]))
                self.assertEqual(str(expected["item_type"]), str(actual["item_type"]))
                self.assertEqual(str(expected["date"]), str(actual["date"]))

    def test_03_get_no_todos_of_date(self) -> None:
        """
        Test retrieving todos for a date with no todos.

        This test performs the following tasks:
        1. Sends a request to the API for a date with no todos.
        2. Checks that the response is an empty list.

        The test ensures that the API correctly returns an empty list when there are no todos for the specified date.
        """

        url = reverse("todos") + "?date=4017-10-28"
        actual = self.client.get(url).data
        self.assertEqual(actual, [])

    def test_04_create_todo_adds_one(self) -> None:
        url = reverse("todos")
        expected = {
            "content": "This is a test",
            "date": "2024-10-28",
        }

        # Checking if the response is correct
        response = self.client.post(url, data=expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Checking if adding one todo adds one to the database (size wise)
        self.assertEqual(self.expected_todos_count + 1, DynamoDB_Manager.get_all_items()[1])
    
    def test_05_create_todos(self) -> None:
        """
        Test the creation of todo items via the API.

        This test verifies that:
        1. Todo items can be created successfully via the POST request.
        2. The response status code is 201 CREATED.
        3. The created items are correctly added to the expected todos.
        5. The total number of items in the database matches the expected count.
        6. The content, completion status, item ID, item type, and date of each item match the expected values.
        """
        url = reverse("todos")
        tasksToCreate = [
            {
                "content": "This is a test",
                "date": "2024-10-28",
            }, 
            {
                "content": "This is a test2",
                "date": "2023-11-28",
            },
            {
                "content": "This is a test3",
                "date": "2023-11-28",
            },
        ]

        # Checking if the response is correct and adding expected todos to all expected todos
        for item in tasksToCreate:
            # Checking if the response is correct
            response = self.client.post(url, data=item)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            if item["date"] not in self.expected_todos:
                self.expected_todos[item["date"]] = []
            self.expected_todos[item["date"]].append(item)

        allDBItems, dbSize  = DynamoDB_Manager.get_all_items()

        self.assertEqual(dbSize, self.expected_todos_count + len(tasksToCreate))
        for key in self.expected_todos.keys():
            for ex, ac in zip(self.expected_todos[key], allDBItems[key]):
                self.assertEqual(str(ex["content"]), str(ac["content"]))
                self.assertFalse(str(ac["completed"]) == True)
                self.assertTrue(ac["item_id"] is not None)
                self.assertEqual("TODO", str(ac["item_type"]))
                self.assertEqual(str(ex["date"]), str(ac["date"]))

    def test_06_create_todo_with_missing_fields(self) -> None:
        """
        Test creating a new todo item with missing fields.

        This test performs the following tasks:
        1. Sends a POST request to the API to create a new todo item with only the 'content' field.
        2. Checks that the response status code is 400 (Bad Request).
        3. Sends a POST request to the API to create a new todo item with only the 'date' field.
        4. Checks that the response status code is 400 (Bad Request).
        5. Sends a POST request to the API to create a new todo item with no fields.
        6. Checks that the response status code is 400 (Bad Request).

        The test ensures that the API correctly returns a 400 status code when required fields are missing in the request data.
        """
        url = reverse("todos")
        actual1 = {
            "content": "This is a test",
        }
        actual2 = {
            "date": "2024-10-28",
        }
        actual3 = {}

        # Checking if the response is correct
        response = self.client.post(url, data=actual1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, data=actual2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, data=actual3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_07_create_duplicate_todo(self) -> None:
        """
        Test creating duplicate todo items.

        This test performs the following tasks:
        1. Sends a POST request to the API to create a new todo item.
        2. Checks that the response status code is 201 (Created).
        3. Sends another POST request to the API to create the same todo item.
        4. Checks that the response status code is 201 (Created).
        5. Verifies that both todo items are present in the response data.
        6. Checks that the fields of the duplicate todo items match the expected values, except for the 'item_id' field which should be unique.

        The test ensures that duplicate todo items can be successfully created and retrieved from the API, and that they have unique 'item_id' fields.
        """
        url = reverse("todos")
        
        expected = {
            "content": "This is a test",
            "date": "2024-10-28",
        }

        # Adding the expected todo twice the expected todos
        self.expected_todos["2024-10-28"].append(expected)
        self.expected_todos["2024-10-28"].append(expected)

        # Sorting the expected todos by content
        self.expected_todos["2024-10-28"].sort(key=lambda d: d["content"])

        # Checking if the response is correct when creating two of the same todos
        response = self.client.post(url, data=expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data=expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        actualItems, actualSize = DynamoDB_Manager.get_all_items()

        # Checking if the size is correct
        self.assertEqual(actualSize, self.expected_todos_count + 2)

        for date in self.expected_todos.keys():
            for ex, ac in zip(self.expected_todos[date], actualItems[date]):
                self.assertEqual(str(ex["content"]), str(ac["content"]))
                self.assertFalse(str(ac["completed"]) == True)
                self.assertTrue(ac["item_id"] is not None)
                self.assertEqual("TODO", str(ac["item_type"]))
                self.assertEqual(str(ex["date"]), str(ac["date"]))
        
    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clearing DynamoDB Database after testing
        """
        super(TodosTests, cls).tearDownClass()
        DynamoDB_Manager.clear_table()
