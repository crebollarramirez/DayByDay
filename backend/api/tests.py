from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from .Dynamo import DynamoDB_Manager
import csv
import os


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
    Test case for CRUD operations on todos using the DynamoDB backend.
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

        self.expected_todos = []
        self.dates = []

        with open(parentDir + "/test_data/todos_test_data.csv", mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert the completed field to a boolean
                row["completed"] = row["completed"] == "True"
                self.expected_todos.append(row)
                if row["item_date"] not in self.dates:
                    self.dates.append(row["item_date"])

        self.expected_todos.sort(key=lambda x: x.get("content", ""))

        # Adding dummy data to database
        DynamoDB_Manager.addDummyData()

    def test_01_length_of_todos(self) -> None:
        """z
        Test the length of todos for each date.

        This test performs the following tasks:
        1. Adds dummy data to the DynamoDB database.
        2. Retrieves todos from the API for each date in the todos dictionary.
        3. Compares the length of the retrieved todos with the length of the todos for each date.

        This test ensures that GET request does not change the size of the database, and retreieve the correct number of todos.
        """

        actual = {}

        for date in self.dates:
            url = reverse("todos") + f"?date={date}"
            actual[date] = self.client.get(url).data
            actual[date].sort(key=lambda d: d["content"])  # Sort by 'content'

        for date in self.dates:
            self.assertEqual(
                len(actual[date]),
                len([x for x in self.expected_todos if x["item_date"] == date]),
            )

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
        for date in self.dates:
            url = reverse("todos") + f"?date={date}"
            actual = self.client.get(url).data
            actual.sort(key=lambda d: d["content"])  # Sort by 'content'
            expected = [x for x in self.expected_todos if x["item_date"] == date]

            # Checking if we got the right todos for the date given
            for expected, actual in zip(actual, expected):
                self.assertEqual(str(expected["content"]), str(actual["content"]))
                self.assertEqual(str(expected["completed"]), str(actual["completed"]))
                self.assertEqual(str(expected["item_id"]), str(actual["item_id"]))
                self.assertEqual(str(expected["item_type"]), str(actual["item_type"]))
                self.assertEqual(str(expected["item_date"]), str(actual["item_date"]))

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
        """
        Test creating a single todo item via the API.

        This test verifies that:
        1. A todo item can be created successfully via a POST request.
        2. The response status code is 201 CREATED.
        3. The total number of items in the database increases by one.
        """
        url = reverse("todos")
        expected = {
            "content": "This is a test",
            "item_date": "2024-10-28",
        }

        # Checking if the response is correct
        response = self.client.post(url, data=expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Checking if adding one todo adds one to the database (size wise)
        self.assertEqual(
            len(self.expected_todos) + 1, len(DynamoDB_Manager.get_all_items())
        )

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
                "item_date": "2024-10-28",
            },
            {
                "content": "This is a test2",
                "item_date": "2023-11-28",
            },
            {
                "content": "This is a test3",
                "item_date": "2023-11-28",
            },
        ]

        # Checking if the response is correct and adding expected todos to all expected todos
        for item in tasksToCreate:
            # Checking if the response is correct
            response = self.client.post(url, data=item)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.expected_todos.append(item)
            self.expected_todos.sort(key=lambda x: x.get("content", ""))

        allDBItems = DynamoDB_Manager.get_all_items()
        self.assertEqual(len(allDBItems), len(self.expected_todos))
        for ex, ac in zip(self.expected_todos, allDBItems):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertFalse(str(ac["completed"]) == True)
            self.assertTrue(ac["item_id"] is not None)
            self.assertEqual("TODO", str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

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
            "item_date": "2024-10-28",
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
            "item_date": "2024-10-28",
        }

        # Adding the expected todo twice the expected todos
        self.expected_todos.append(expected)
        self.expected_todos.append(expected)

        # Sorting the expected todos by content
        self.expected_todos.sort(key=lambda d: d["content"])

        # Checking if the response is correct when creating two of the same todos
        response = self.client.post(url, data=expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data=expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        actualItems = DynamoDB_Manager.get_all_items()

        # Checking if the size is correct
        self.assertEqual(len(actualItems), len(self.expected_todos))

        for ex, ac in zip(self.expected_todos, actualItems):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertFalse(str(ac["completed"]) == True)
            self.assertTrue(ac["item_id"] is not None)
            self.assertEqual("TODO", str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    def test_08_delete_only_todo_in_date(self) -> None:
        """
        Test case for deleting the only todo item on a specific date.

        This test verifies that deleting the only todo item on a specific date
        correctly removes the item from the expected todos and the database.

        Steps:
        1. Set the ITEM_ID of the todo to be deleted.
        2. Construct the URL for the delete request.
        3. Remove the item from the expected todos dictionary.
        4. Send a DELETE request to the server.
        5. Verify the response status code is 200 OK.
        6. Retrieve all items from the database.
        7. Verify the size of the database has decreased by one.
        8. Verify the remaining items in the database match the expected todos.

        Asserts:
        - The response status code is 200 OK.
        - The size of the database is reduced by one.
        - The remaining items in the database match the expected todos.
        """
        ITEM_ID = "3"
        url = reverse("todos") + f"?item_id={ITEM_ID}"

        # Checking if the response is correct
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Deleting the item from the expected todos
        for ex in self.expected_todos:
            if ex["item_id"] == ITEM_ID:
                self.expected_todos.remove(ex)
                break

        actualItems = DynamoDB_Manager.get_all_items()

        # Checking if deleting one todo removes one from the database (size wise)
        self.assertEqual(len(self.expected_todos), len(actualItems))

        for ex, ac in zip(self.expected_todos, actualItems):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertFalse(str(ex["completed"]) == True, str(ac["completed"]) == True)
            self.assertTrue(ac["item_id"] is not None)
            self.assertEqual("TODO", str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    # Trying to delete an item that does not exist or "wrong id"

    def test_09_delete_non_existent_todo(self) -> None:
        """
        Test case for attempting to delete a non-existent todo item.

        This test verifies that attempting to delete a todo item that does not exist
        results in the appropriate error response from the server.

        Steps:
        1. Set the ITEM_ID of the non-existent todo to be deleted.
        2. Construct the URL for the delete request.
        3. Send a DELETE request to the server.
        4. Verify the response status code is 400 BAD REQUEST.

        Asserts:
        - The response status code is 400 BAD REQUEST.
        """
        ITEM_ID = "696969"
        url = reverse("todos") + f"?item_id={ITEM_ID}"

        # Checking if the response is correct
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Deleting multiple items
    def test_10_delete_multiple_todos(self) -> None:
        """
        Test case for deleting multiple todo items.

        This test verifies that deleting multiple todo items correctly removes the items
        from the expected todos and the database.

        Steps:
        1. Set the ITEM_IDS of the todos to be deleted.
        2. Iterate through the expected todos and remove the items with matching ITEM_IDS.
        3. Remove any dates that have an empty list of todos.
        4. Send a DELETE request to the server for each ITEM_ID.
        5. Verify the response status code is 200 OK for each request.
        6. Retrieve all items from the database.
        7. Verify the size of the database has decreased by the number of deleted items.
        8. Verify the remaining items in the database match the expected todos.

        Asserts:
        - The response status code is 200 OK for each DELETE request.
        - The size of the database is reduced by the number of deleted items.
        - The remaining items in the database match the expected todos.
        """
        ITEM_IDS = ("1", "8", "3")

        # Removing the items from the expected todos
        for item_id in ITEM_IDS:
            for item in self.expected_todos:
                if item["item_id"] == item_id:
                    self.expected_todos.remove(item)
                    break

        # Deleting the items
        for item_id in ITEM_IDS:
            url = reverse("todos") + f"?item_id={item_id}"

            # Checking if the response is correct
            response = self.client.delete(url)
            actualItems = DynamoDB_Manager.get_all_items()
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking if deleting one todo removes one from the database (size wise)
        self.assertEqual(len(self.expected_todos), len(actualItems))

        # Checking if the items are deleted and other items are not
        for ex, ac in zip(self.expected_todos, actualItems):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertFalse(str(ac["completed"]) == True)
            self.assertTrue(ac["item_id"] is not None)
            self.assertEqual("TODO", str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    # Deleting an item then deleting it again
    def test_11_delete_todo_twice(self) -> None:
        """
        Test case for deleting a todo item twice.

        This test verifies that deleting a todo item twice results in the appropriate
        responses from the server.

        Steps:
        1. Set the ITEM_ID of the todo to be deleted.
        2. Construct the URL for the delete request.
        3. Send a DELETE request to the server.
        4. Verify the response status code is 200 OK.
        5. Send a DELETE request to the server again for the same ITEM_ID.
        6. Verify the response status code is 400 BAD REQUEST.
        7. Verifies if the size of the database remains unchanged after the second delete request.

        Asserts:
        - The response status code is 200 OK for the first DELETE request.
        - The response status code is 400 BAD REQUEST for the second DELETE request.
        """
        ITEM_ID = "10"

        # Removing the item from the expected todos
        for item in self.expected_todos:
            if item["item_id"] == ITEM_ID:
                self.expected_todos.remove(item)
                break

        url = reverse("todos") + f"?item_id={ITEM_ID}"

        # Checking if the response is correct
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking if the response is correct
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Checking if the size was not changed
        actualItems = DynamoDB_Manager.get_all_items()
        self.assertEqual(len(self.expected_todos), len(actualItems))

    def test_12_delete_todos_multiple_in_dates(self) -> None:
        """
        Test case for deleting multiple todo items on the same date.

        This test verifies that deleting multiple todo items on the same date
        correctly removes the items from the expected todos and the database.

        Steps:
        1. Set the ITEM_IDS of the todos to be deleted.
        2. Iterate through the expected todos and remove the items with matching ITEM_IDS.
        3. Send a DELETE request to the server for each ITEM_ID.
        4. Verify the response status code is 200 OK for each request.
        5. Retrieve all items from the database.
        6. Verify the size of the database has decreased by the number of deleted items.
        7. Verify the remaining items in the database match the expected todos.

        Asserts:
        - The response status code is 200 OK for each DELETE request.
        - The size of the database is reduced by the number of deleted items.
        - The remaining items in the database match the expected todos.
        """
        ITEM_IDS = ("11", "6")

        for item_id in ITEM_IDS:
            for ex in self.expected_todos:
                if ex["item_id"] == item_id:
                    self.expected_todos.remove(ex)
                    break

        for item_id in ITEM_IDS:
            url = reverse("todos") + f"?item_id={item_id}"

            # Checking if the response is correct
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking if deleting one todo removes one from the database (size wise)
        actualItems = DynamoDB_Manager.get_all_items()
        self.assertEqual(len(self.expected_todos), len(actualItems))

        for ex, ac in zip(self.expected_todos, actualItems):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertFalse(str(ac["completed"]) == True)
            self.assertTrue(ac["item_id"] is not None)
            self.assertEqual("TODO", str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    def test_13_delete_todos_multiple_in_different_dates(self) -> None:
        """
        Test case for deleting multiple todo items on different dates.

        This test verifies that deleting multiple todo items on different dates
        correctly removes the items from the expected todos and the database.

        Steps:
        1. Set the ITEM_IDS of the todos to be deleted.
        2. Iterate through the expected todos and remove the items with matching ITEM_IDS.
        3. Send a DELETE request to the server for each ITEM_ID.
        4. Verify the response status code is 200 OK for each request.
        5. Retrieve all items from the database.
        6. Verify the size of the database has decreased by the number of deleted items.
        7. Verify the remaining items in the database match the expected todos.

        Asserts:
        - The response status code is 200 OK for each DELETE request.
        - The size of the database is reduced by the number of deleted items.
        - The remaining items in the database match the expected todos.
        """
        ITEM_IDS = ("10", "11", "5", "2", "6", "12")
        for item_id in ITEM_IDS:
            for ex in self.expected_todos:
                if ex["item_id"] == item_id:
                    self.expected_todos.remove(ex)
                    break

        for item_id in ITEM_IDS:
            url = reverse("todos") + f"?item_id={item_id}"
            # Checking if the response is correct
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking if deleting one todo removes one from the database (size wise)
        actualItems = DynamoDB_Manager.get_all_items()

        # Checking if the size is correct after deleting multiple items
        self.assertEqual(len(self.expected_todos), len(actualItems))

        # Now checking if all other items were not altered.
        for ex, ac in zip(self.expected_todos, actualItems):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertFalse(str(ac["completed"]) == True)
            self.assertTrue(ac["item_id"] is not None)
            self.assertEqual("TODO", str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    def test_14_update_todo_none(self) -> None:
        """
        Test case for updating a todo item with no changes.

        This test verifies that updating a todo item with no changes
        correctly returns a 200 OK response and does not alter the database.

        Steps:
        1. Set the ITEM_ID of the todo to be updated.
        2. Construct the URL for the update request.
        3. Send a PUT request to the server with no changes.
        4. Verify the response status code is 200 OK.
        5. Retrieve all items from the database.
        6. Verify the size of the database remains unchanged.
        7. Verify the remaining items in the database match the expected todos.

        Asserts:
        - The response status code is 200 OK.
        - The size of the database remains unchanged.
        - The remaining items in the database match the expected todos.
        """
        ITEM_ID = "1"
        url = reverse("todos") + f"?item_id={ITEM_ID}"

        # Checking if the response is correct
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking if the size was not changed
        actualItems = DynamoDB_Manager.get_all_items()
        self.assertEqual(len(self.expected_todos), len(actualItems))
        for ex, ac in zip(self.expected_todos, actualItems):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertFalse(str(ac["completed"]) == True)
            self.assertTrue(ac["item_id"] is not None)
            self.assertEqual("TODO", str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    def test_15_update_todo_completed(self) -> None: 
        """
        Test case for updating the 'completed' status of a todo item.

        This test updates the 'completed' status of a todo item with a specific ITEM_ID
        and verifies that the update is successful by checking the response status code
        and comparing the updated 'completed' status with the expected status in the database.

        Steps:
        1. Define the ITEM_ID and construct the URL for the PUT request.
        2. Send a PUT request to update the 'completed' status of the todo item.
        3. Verify that the response status code is HTTP 200 OK.
        4. Update the expected 'completed' status in the local expected_todos list.
        5. Retrieve the actual items from the database.
        6. Compare the expected and actual items to ensure they match.

        Asserts:
        - The response status code is HTTP 200 OK.
        - The content, completed status, item_id, item_type, and item_date of each item in the
        expected_todos list match the corresponding values in the actual items retrieved from the database.
        """
        ITEM_ID = "7"
        url = reverse("todos") + f"?item_id={ITEM_ID}"

        response = self.client.put(url, data={"completed": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in self.expected_todos:
            if item["item_id"] == ITEM_ID:
                item["completed"] = True
                break

        # Now getting the actual and seeing if it is the same as expected
        actual = DynamoDB_Manager.get_all_items()
        for ex, ac in zip(self.expected_todos, actual):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertEqual(ex["completed"], ac["completed"])
            self.assertEqual(str(ex["item_id"]), str(ac["item_id"]))
            self.assertEqual(str(ex["item_type"]), str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    def test_16_update_todo_content(self) -> None:
        """
        Test case for updating the content of a todo item.

        This test updates the content of a todo item with a specific ITEM_ID
        and verifies that the update is successful by checking the response
        status code and comparing the updated content with the expected content
        in the database.

        Steps:
        1. Define the ITEM_ID and construct the URL for the PUT request.
        2. Send a PUT request to update the content of the todo item.
        3. Verify that the response status code is HTTP 200 OK.
        4. Update the expected content in the local expected_todos list.
        5. Sort the expected_todos list by content.
        6. Retrieve the actual items from the database.
        7. Compare the expected and actual items to ensure they match.

        Asserts:
        - The response status code is HTTP 200 OK.
        - The content, item_id, item_type, and item_date of each item in the
        expected_todos list match the corresponding values in the actual items
        retrieved from the database.
        """
        ITEM_ID = "2"
        url = reverse("todos") + f"?item_id={ITEM_ID}"

        response = self.client.put(url, data={"content": "This is a new content"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in self.expected_todos:
            if item["item_id"] == ITEM_ID:
                item["content"] = "This is a new content"
                break
        
        # need to resort the expected todos after changing the content
        self.expected_todos.sort(key=lambda x: x.get("content", ""))

        # Now getting the actual and seeing if it is the same as expected
        actual = DynamoDB_Manager.get_all_items()
        for ex, ac in zip(self.expected_todos, actual):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertEqual(str(ex["item_id"]), str(ac["item_id"]))
            self.assertEqual(str(ex["item_type"]), str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    def test_17_update_todo_date(self) -> None:
        """
        Test case for updating the date of a todo item.

        This test updates the date of a specific todo item identified by ITEM_ID.
        It sends a PUT request to the "todos" endpoint with the new date.
        The test then verifies that the response status code is HTTP 200 OK.
        After updating the date, it resorts the expected todos list.
        Finally, it retrieves all items from DynamoDB and compares each field
        of the expected todos with the actual items to ensure they match.

        Assertions:
            - The response status code is HTTP 200 OK.
            - The content, item_id, item_type, and item_date of each expected todo
            match the corresponding fields of the actual items retrieved from DynamoDB.
        """
        ITEM_ID = "11"
        url = reverse("todos") + f"?item_id={ITEM_ID}"

        response = self.client.put(url, data={"item_date": "2021-11-28"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in self.expected_todos:
            if item["item_id"] == ITEM_ID:
                item["item_date"] = "2021-11-28"
                break

        # need to resort the expected todos after changing the date
        self.expected_todos.sort(key=lambda x: x.get("content", ""))

        # Now getting the actual and seeing if it is the same as expected
        actual = DynamoDB_Manager.get_all_items()
        for ex, ac in zip(self.expected_todos, actual):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertEqual(str(ex["item_id"]), str(ac["item_id"]))
            self.assertEqual(str(ex["item_type"]), str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    def test_18_update_multiple_todos(self) -> None:
        """
        Test case for updating multiple todo items.

        This test updates multiple todo items identified by ITEM_IDS.
        It sends multiple PUT requests to the "todos" endpoint with the new data.
        The test then verifies that the response status code for each request is HTTP 200 OK.
        After updating the items, it resorts the expected todos list.
        Finally, it retrieves all items from DynamoDB and compares each field
        of the expected todos with the actual items to ensure they match.

        Assertions:
            - The response status code for each PUT request is HTTP 200 OK.
            - The content, item_id, item_type, and item_date of each expected todo
            match the corresponding fields of the actual items retrieved from DynamoDB.
        """
        ITEM_IDS = ("1", "2", "3", "9")

        for item in self.expected_todos:
            if str(item["item_id"]) == ITEM_IDS[0]:
                item["completed"] = True
                item["content"] = "This is a new edited content"
                item["item_date"] = "2019-07-05"
            if item["item_id"] == ITEM_IDS[1]:
                item["completed"] = True
            if item["item_id"] == ITEM_IDS[2]:
                item["content"] = "only edited the content"
            if item["item_id"] == ITEM_IDS[3]:
                item["item_date"] = "2025-01-28"

        # Need to sort again
        self.expected_todos.sort(key=lambda x: x.get("content", ""))


        url = reverse("todos") + f"?item_id={ITEM_IDS[0]}"
        response = self.client.put(url, data={"completed": True, "content": "This is a new edited content", "item_date": "2019-07-05"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("todos") + f"?item_id={ITEM_IDS[1]}"
        response = self.client.put(url, data={"completed": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("todos") + f"?item_id={ITEM_IDS[2]}"
        response = self.client.put(url, data={"content": "only edited the content"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("todos") + f"?item_id={ITEM_IDS[3]}"
        response = self.client.put(url, data={"item_date": "2025-01-28"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now getting the actual and seeing if it is the same as expected
        actual = DynamoDB_Manager.get_all_items()
        for ex, ac in zip(self.expected_todos, actual):
            self.assertEqual(str(ex["content"]), str(ac["content"]))
            self.assertEqual(str(ex["item_id"]), str(ac["item_id"]))
            self.assertEqual(str(ex["item_type"]), str(ac["item_type"]))
            self.assertEqual(str(ex["item_date"]), str(ac["item_date"]))

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clearing DynamoDB Database after testing
        """
        super(TodosTests, cls).tearDownClass()
        DynamoDB_Manager.clear_table()
