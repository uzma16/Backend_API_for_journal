from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Journal

User = get_user_model()

class JournalAPITestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create some test journals for the user
        Journal.objects.create(user=self.user, title="Journal 1", description="First journal")
        Journal.objects.create(user=self.user, title="Journal 2", description="Second journal")

        # Set up the test client
        self.client = APIClient()

    def test_list_journals(self):
        # Authenticate the test client with the test user
        self.client.force_authenticate(user=self.user)

        # Send a GET request to the 'journal-list' URL
        url = reverse("journal-list")
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains the correct number of journals
        self.assertEqual(len(response.data), 2)

    def test_create_journal(self):
        # Authenticate the test client with the test user
        self.client.force_authenticate(user=self.user)

        # Data for the new journal
        data = {
            "title": "New Journal",
            "description": "This is a new journal",
        }

        # Send a POST request to the 'journal-list' URL to create a new journal
        url = reverse("journal-list")
        response = self.client.post(url, data, format="json")

        # Check that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the new journal was created in the database
        self.assertEqual(Journal.objects.count(), 3)

        # Check that the journal belongs to the test user
        new_journal = Journal.objects.get(id=response.data["id"])
        self.assertEqual(new_journal.user, self.user)

    def test_retrieve_journal(self):
        # Authenticate the test client with the test user
        self.client.force_authenticate(user=self.user)

        # Get the ID of the first journal created by the test user
        journal_id = Journal.objects.filter(user=self.user).first().id

        # Send a GET request to the 'journal-detail' URL with the journal ID
        url = reverse("journal-detail", args=[journal_id])
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the returned journal data matches the expected data
        expected_data = {
            "id": str(journal_id),
            "title": "Journal 1",
            "description": "First journal",
            # Add other expected fields here
        }
        self.assertEqual(response.data, expected_data)

    def test_update_journal(self):
        # Authenticate the test client with the test user
        self.client.force_authenticate(user=self.user)

        # Get the ID of the first journal created by the test user
        journal_id = Journal.objects.filter(user=self.user).first().id

        # Data for updating the journal
        data = {
            "title": "Updated Journal",
            "description": "This journal has been updated.",
            # Add other fields to be updated
        }

        # Send a PUT request to the 'journal-detail' URL with the journal ID to update the journal
        url = reverse("journal-detail", args=[journal_id])
        response = self.client.put(url, data, format="json")

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the journal in the database has been updated with the new data
        updated_journal = Journal.objects.get(id=journal_id)
        self.assertEqual(updated_journal.title, "Updated Journal")
        self.assertEqual(updated_journal.description, "This journal has been updated.")
        # Check other updated fields here

    def test_delete_journal(self):
        # Authenticate the test client with the test user
        self.client.force_authenticate(user=self.user)

        # Get the ID of the first journal created by the test user
        journal_id = Journal.objects.filter(user=self.user).first().id

        # Send a DELETE request to the 'journal-detail' URL with the journal ID to delete the journal
        url = reverse("journal-detail", args=[journal_id])
        response = self.client.delete(url)

        # Check that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the journal has been deleted from the database
        self.assertEqual(Journal.objects.count(), 1)



