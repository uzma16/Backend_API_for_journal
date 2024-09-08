from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginTestCase(TestCase):
    def setUp(self):
        # Create a user with a valid phone number and password
        self.user = User.objects.create(phone="9171167347", password="aman123")

        # URL for the login view
        self.login_url = reverse("login POST")

    def test_standard_login_successful(self):
        # Valid login credentials
        data = {
            "phone": "9171167347",
            "password": "aman123",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure that the response contains the JWT tokens
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_standard_login_invalid_credentials(self):
        # Invalid login credentials
        data = {
            "phone": "1234567890",
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Write similar test cases for third-party login (e.g., Firebase) if applicable
    # You might need to mock the Firebase authentication to simulate the response

    # Example for Firebase (you'll need to implement Firebase mock)
    def test_firebase_login_successful(self):
        # Mock the Firebase response for a successful login
        # firebase_response = your_mocked_firebase_response()

        data = {
            "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImIyZGZmNzhhMGJkZDVhMDIyMTIwNjM0OTlkNzdlZjRkZWVkMWY2NWIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbWluZGZ1bG5lc3MtNWMyYjQiLCJhdWQiOiJtaW5kZnVsbmVzcy01YzJiNCIsImF1dGhfdGltZSI6MTY5MDIwMzQ4MSwidXNlcl9pZCI6Im1kdDhkdkp6NjVZMXowcWtCUVczenZoZGZ4OTIiLCJzdWIiOiJtZHQ4ZHZKejY1WTF6MHFrQlFXM3p2aGRmeDkyIiwiaWF0IjoxNjkwMjAzNDgxLCJleHAiOjE2OTAyMDcwODEsInBob25lX251bWJlciI6Iis5MTk4NzY1NDMyMTAiLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7InBob25lIjpbIis5MTk4NzY1NDMyMTAiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwaG9uZSJ9fQ.H65AwmAmb2gfAIeVhfRCqEa3Ih3IP3fU8pG58gu5YYPGdusG4msP9B3V0thqGWy2NCO1969OG1tuD_joo-pyI0XXbHHvMcNf0ek7xEtaX2MptPa1HDbnQ_XIoz8xOlUgVCdFyX6hFp4YujeX-GmRB9vOdh55S1W48CKA0YT_ebJHzFotKgoARFZ4sS-64QslpAtgIk6aewcwx1wxlZi4DNs3YT6AIe7R1t_q0Cg7cI6ugUzE4HeUhBTv9IJuV-mvvUw--p3ktpOi-v8aPqyAOJWj3Pd1GqfdFC2O-LgExyK7ihF9ORxWh66XCxmpzrksg_kfMz-Cn8f_AWYNej3mDw",
            "fcm_token": "dJc4oyEiTo-Tco4DtzDn2-:APA91bHafj78zQ2PwcaRFANmFSp_e0hZdkPzbcfMHuXZm0PwpgWEhT-G9wIRvOFAls4PoY7OqLK4V1iMEK4jgbSgga-PCk0CpDGGiwk0GTGslVMadf7bpenRjSMB7Z75d96qR3QgEnU4",
            "timezone": "UTC +5:30",
            "timezone_name": "Asia/Kolkata",
        }

        response = self.client.post(reverse("third party login POST"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

#----------------------------------------------------------------------------------#
class UserRegistrationTestCase(TestCase):
    def setUp(self):
        # URL for the registration view
        self.registration_url = reverse("register POST")

    def test_registration_successful(self):
        # Valid registration data
        data = {
            "phone": "9171167347",
            "password": "aman123",
            # Add other required fields if applicable
        }
        response = self.client.post(self.registration_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the user was created in the database
        self.assertTrue(User.objects.filter(phone="1234567890").exists())

    def test_registration_duplicate_phone_number(self):
        # Create a user with a duplicate phone number
        User.objects.create(phone="1234567890", password="testpassword")

        # Attempt to register with the same phone number
        data = {
            "phone": "1234567890",
            "password": "anotherpassword",
            # Add other required fields if applicable
        }
        response = self.client.post(self.registration_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["phone"][0], "A user with this phone number already exists.")


    def test_registration_missing_required_fields(self):
        # Attempt to register without providing required fields
        data = {
            # Missing phone number and password
            # Add other required fields that are missing
        }
        response = self.client.post(self.registration_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert for specific error messages returned for each missing field

     #----------------------------------------------------------------------- # 

class UserProfileManagementTestCase(TestCase):
    def setUp(self):
        # Create a user with profile data
        self.user = User.objects.create(
            phone="1234567890",
            password="testpassword",
            full_name="John Doe",
            date_of_birth="1990-01-01",
            gender="male",
        )

        # URL for the user profile detail view
        self.profile_url = reverse("user-detail", args=[self.user.id])

    def test_update_profile_successful(self):
        # Updated profile data
        data = {
            "full_name": "Jane Doe",
            "date_of_birth": "1985-05-05",
            "gender": "female",
            # Include other fields you want to update
        }
        self.client.login(phone="1234567890", password="testpassword")
        response = self.client.patch(self.profile_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh user data from the database
        self.user.refresh_from_db()
        
        # Check if the user profile was updated in the database
        self.assertEqual(self.user.full_name, "Jane Doe")
        self.assertEqual(str(self.user.date_of_birth), "1985-05-05")
        self.assertEqual(self.user.gender, "female")
        # Check other fields as needed

    def test_update_profile_unauthenticated(self):
        # Attempt to update profile without authentication
        data = {
            "full_name": "Jane Doe",
            "date_of_birth": "1985-05-05",
            "gender": "female",
        }
        response = self.client.patch(self.profile_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Refresh user data from the database
        self.user.refresh_from_db()

        # Check that the profile data remains unchanged
        self.assertEqual(self.user.full_name, "John Doe")
        self.assertEqual(str(self.user.date_of_birth), "1990-01-01")
        self.assertEqual(self.user.gender, "male")
        # Check other fields as needed

     #----------------------------------------------------------------------- # 

class UserProfileManagementTestCase(TestCase):
    def setUp(self):
        # Create a user with profile data
        self.user = User.objects.create(
            phone="1234567890",
            password="testpassword",
            full_name="John Doe",
            date_of_birth="1990-01-01",
            gender="male",
        )

        # URL for the user profile detail view
        self.profile_url = reverse("user-detail", args=[self.user.id])

    def test_update_profile_successful(self):
        # Updated profile data
        data = {
            "full_name": "Jane Doe",
            "date_of_birth": "1985-05-05",
            "gender": "female",
            # Include other fields you want to update
        }
        self.client.login(phone="1234567890", password="testpassword")
        response = self.client.patch(self.profile_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh user data from the database
        self.user.refresh_from_db()
        
        # Check if the user profile was updated in the database
        self.assertEqual(self.user.full_name, "Jane Doe")
        self.assertEqual(str(self.user.date_of_birth), "1985-05-05")
        self.assertEqual(self.user.gender, "female")
        # Check other fields as needed

    def test_update_profile_unauthenticated(self):
        # Attempt to update profile without authentication
        data = {
            "full_name": "Jane Doe",
            "date_of_birth": "1985-05-05",
            "gender": "female",
        }
        response = self.client.patch(self.profile_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Refresh user data from the database
        self.user.refresh_from_db()

        # Check that the profile data remains unchanged
        self.assertEqual(self.user.full_name, "John Doe")
        self.assertEqual(str(self.user.date_of_birth), "1990-01-01")
        self.assertEqual(self.user.gender, "male")
        # Check other fields as needed

 #----------------------------------------------------------------------- # 

class JWTTokenGenerationTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(phone="1234567890", password="testpassword")

        # URL for the login and registration views
        self.login_url = reverse("login POST")
        self.registration_url = reverse("register POST")

    def test_jwt_token_generation_on_login(self):
        # Valid login credentials
        data = {
            "phone": "1234567890",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure that the response contains the JWT tokens
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

        # Extract the JWT tokens from the response
        refresh_token = response.data["refresh"]
        access_token = response.data["access"]

        # Verify the JWT tokens and extract user information
        refresh = RefreshToken(refresh_token)
        access = refresh.access_token

        # Verify that the tokens are valid and not expired
        self.assertTrue(refresh_token)
        self.assertTrue(access_token)
        self.assertTrue(refresh.is_valid())
        self.assertTrue(access.is_valid())

        # Extract user information from the JWT tokens
        self.assertEqual(access["user_id"], str(self.user.id))
        # Add other user information you want to verify, e.g., username, phone, etc.

    def test_jwt_token_generation_on_registration(self):
        # Valid registration data
        data = {
            "phone": "9876543210",
            "password": "testpassword",
            # Add other required fields if applicable
        }
        response = self.client.post(self.registration_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure that the response contains the JWT tokens
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

        # Extract the JWT tokens from the response
        refresh_token = response.data["refresh"]
        access_token = response.data["access"]

        # Verify the JWT tokens and extract user information
        refresh = RefreshToken(refresh_token)
        access = refresh.access_token

        # Verify that the tokens are valid and not expired
        self.assertTrue(refresh_token)
        self.assertTrue(access_token)
        self.assertTrue(refresh.is_valid())
        self.assertTrue(access.is_valid())

        # Extract user information from the JWT tokens
        user = User.objects.get(phone=data["phone"])
        self.assertEqual(access["user_id"], str(user.id))
        # Add other user information you want to verify, e.g., username, phone, etc.

    #----------------------------------------------------------------------- # 

class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(phone="1234567890", password="testpassword")

        # Create JWT tokens for authentication
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = self.refresh.access_token

        # URL for the protected view (e.g., UserDetail view)
        self.protected_view_url = reverse("user-detail", args=[self.user.id])

    def test_protected_view_authenticated(self):
        # Make an authenticated request to the protected view using the access token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.protected_view_url)

        # Ensure that the response status code is 200 (HTTP OK) for authenticated user
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected user data or any other desired validation

    def test_protected_view_unauthenticated(self):
        # Make an unauthenticated request to the protected view
        response = self.client.get(self.protected_view_url)

        # Ensure that the response status code is 401 (HTTP Unauthorized) for unauthenticated user
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert that the response contains an appropriate error message or any other desired validation

from unittest.mock import patch

class ThirdPartyLoginTestCase(TestCase):
    def setUp(self):
        # URL for the third-party login view (e.g., LoginWithSocialAuth view)
        self.login_url = reverse("third party login POST")

    @patch('firebase_admin.auth.verify_id_token')
    def test_firebase_login_successful(self, mock_verify_id_token):
        # Mock the response from Firebase verify_id_token
        mock_verify_id_token.return_value = {
            "phone_number": "+1234567890",
            "email": "test@example.com",
            # Include other user information as needed
        }

        # Provide the necessary data for the login request
        data = {
            "id_token": "test_id_token_from_firebase",
            "fcm_token": "test_fcm_token",
            "timezone": "UTC",
            "timezone_name": "Coordinated Universal Time",
        }

        # Send a POST request to the third-party login view
        response = self.client.post(self.login_url, data, format="json")

        # Ensure that the response status code is 200 (HTTP OK) for successful login
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the JWT tokens or any other desired validation

    @patch('jwt.decode')
    def test_invalid_id_token_from_firebase(self, mock_jwt_decode):
        # Mock the response from jwt.decode to simulate an invalid ID token
        mock_jwt_decode.side_effect = jwt.InvalidTokenError

        # Provide the necessary data for the login request
        data = {
            "id_token": "invalid_id_token_from_firebase",
            "fcm_token": "test_fcm_token",
            "timezone": "UTC",
            "timezone_name": "Coordinated Universal Time",
        }

        # Send a POST request to the third-party login view
        response = self.client.post(self.login_url, data, format="json")

        # Ensure that the response status code is 401 (HTTP Unauthorized) for invalid ID token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #----------------------------------------------------------------------- # 

class UserProfileAPITestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(phone="1234567890", password="testpassword")

        # URL for the user profile detail view (e.g., UserDetail view)
        self.profile_detail_url = reverse("user-detail", args=[self.user.id])

    def test_get_user_profile_successful(self):
        # Send a GET request to the user profile detail view
        response = self.client.get(self.profile_detail_url)

        # Ensure that the response status code is 200 (HTTP OK) for successful request
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the expected user profile data
        self.assertEqual(response.data["id"], str(self.user.id))
        # Add other assertions to check user profile fields such as username, phone, full_name, etc.

    def test_get_user_profile_invalid_user_id(self):
        # URL for an invalid user_id
        invalid_user_id_url = reverse("user-detail", args=[999])

        # Send a GET request to an invalid user_id URL
        response = self.client.get(invalid_user_id_url)

        # Ensure that the response status code is 404 (HTTP Not Found) for invalid user_id
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        #----------------------------------------------------------------------- # 

class PermissionTestCase(TestCase):
    def setUp(self):
        # Create a regular user for testing
        self.user = User.objects.create_user(phone="1234567890", password="testpassword")

        # Create a superuser for testing
        self.superuser = User.objects.create_superuser(phone="9876543210", password="testpassword")

        # URL for the view that requires superuser permission (e.g., some_admin_view)
        self.admin_view_url = reverse("some_admin_view")

        # URL for the view that requires staff permission (e.g., some_staff_view)
        self.staff_view_url = reverse("some_staff_view")

    def test_superuser_access_to_admin_view(self):
        # Set the superuser as the client's user
        self.client.force_login(self.superuser)

        # Send a GET request to the view that requires superuser permission
        response = self.client.get(self.admin_view_url)

        # Ensure that the response status code is 200 (HTTP OK) for superuser access
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Add other assertions to check the response data or other desired validation for superuser access

    def test_regular_user_denied_access_to_admin_view(self):
        # Set the regular user as the client's user
        self.client.force_login(self.user)

        # Send a GET request to the view that requires superuser permission
        response = self.client.get(self.admin_view_url)

        # Ensure that the response status code is 403 (HTTP Forbidden) for regular user access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Add other assertions to check the response data or other desired validation for regular user access

    def test_staff_access_to_staff_view(self):
        # Set the superuser as the client's user (staff members are superusers by default)
        self.client.force_login(self.superuser)

        # Send a GET request to the view that requires staff permission
        response = self.client.get(self.staff_view_url)

        # Ensure that the response status code is 200 (HTTP OK) for staff access
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Add other assertions to check the response data or other desired validation for staff access

    def test_regular_user_denied_access_to_staff_view(self):
        # Set the regular user as the client's user
        self.client.force_login(self.user)

        # Send a GET request to the view that requires staff permission
        response = self.client.get(self.staff_view_url)

        # Ensure that the response status code is 403 (HTTP Forbidden) for regular user access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #----------------------------------------------------------------------- # 

class ErrorHandlingTestCase(TestCase):
    def setUp(self):
        # URL for the user login view (e.g., UserLogin view)
        self.login_url = reverse("login POST")

    def test_missing_input_fields(self):
        # Send a POST request with missing required fields (e.g., no id_token or fcm_token)
        data = {
            # Missing required fields: 'id_token', 'fcm_token', 'timezone', 'timezone_name'
        }
        response = self.client.post(self.login_url, data, format="json")

        # Ensure that the response status code is 400 (HTTP Bad Request) for missing input fields
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Add other assertions to check the response data or error messages for missing input fields

    def test_invalid_id_token(self):
        # Send a POST request with an invalid id_token
        data = {
            "id_token": "invalid_id_token",
            "fcm_token": "test_fcm_token",
            "timezone": "UTC",
            "timezone_name": "Coordinated Universal Time",
        }
        response = self.client.post(self.login_url, data, format="json")

        # Ensure that the response status code is 401 (HTTP Unauthorized) for invalid id_token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

     

