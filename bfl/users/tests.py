from django.test import TestCase
from django.urls import reverse
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User

password = 'mypassword' # Global password to be used in tests

def create_user(first_name='Test', last_name='User', username='myuser', email='myemail@test.com'):
    """
    Create a new user given the basic user information: the user's first name,
    the user's last name, the user's username, and the user's email.
    """
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    return user

def create_profile(user):
    """
    Create a profile for the given user.
    """
    profile = Profile(user=user)
    profile.save()
    return profile

class ProfileModelTests(TestCase):
    def test_profile_creation(self):
        """
        Test that a profile is properly created for a user.
        """
        user = create_user() # Create the user
        profile = create_profile(user=user) # Create the profile for the user
        self.assertTrue(isinstance(profile, Profile)) # Make sure the profile is an instance of Profile
        self.assertEqual(user.profile, profile) # Make sure that the profile is associated to the user
        self.assertEqual(profile.__str__(), f'{user.username} Profile') # Make sure that the profile prints correctly

    def test_user_default_picture(self):
        """
        When a user creates an account and profile, the default profile picture should be "default.jpeg".
        """
        user = create_user() # Create the user
        profile = create_profile(user=user) # Create the profile for the user
        self.assertEqual(user.profile.image.url, "/media/default.jpeg") # Make sure the default profile picture is the default.jpeg

class UserCreationTests(TestCase):

    def test_register_user(self):
        """
        Test that a user is able to create an account properly by checking if the user is in the database after the account is created.
        """
        my_user = create_user() # Create a user
        my_user_from_database = User.objects.get(username="myuser") # Grab from the database the user
        self.assertEqual(my_user, my_user_from_database) # Compare the users to see if they are the same
        self.assertTrue(my_user.is_active) # Make sure when user is created they are equal
        self.assertFalse(my_user.is_staff) # Make sure that the user does not have admin status
        self.assertFalse(my_user.is_superuser)

    def test_duplicate_user_username(self):
        """
        Test that a user is not able to create an account with the same username as a user that is already created.
        """
        my_user = create_user() # Create an initial user
        try:
            my_second_user = create_user(first_name='John', last_name="Doe", email="johndoe@example.com") # Create a duplicate user with the same username
        except Exception as e:
            pass # if exception is raised, that is a good sign
        else:
            self.assertNotEqual(my_user.username, my_second_user.username) # Check if the usernames for both of the users are equal if an error isnt raised

class UserRegisterFormTests(TestCase):

    def test_duplicate_user_email(self):
        """
        Test that a user is not able to create an account with the same email as a user that is already created.
        """
        my_user = create_user() # Create the first user
        form_data = { # Add information to the form to test duplicate email
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': my_user.email,
            'password1': password,
            'password2': password,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid()) # Should return false since there shouldnt be two users with the same email

    def test_duplicate_user_username(self):
        """
        Test that a user is not able to create an account with the same username as a user that is already created.
        """
        my_user = create_user() # Create the first user
        form_data = { # Add information to the form to test duplicate email
            'first_name': 'John',
            'last_name': 'Doe',
            'username': my_user.username,
            'email': 'johndoe@example.com',
            'password1': password,
            'password2': password,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid()) # Should return false since there shouldnt be two users with the same email

class UserUpdateFormTests(TestCase):

    def test_duplicate_user_email(self):
        """
        Test that a user is not able to create an account with the same email as a user that is already created.
        """
        my_user = create_user() # Create the first user
        form_data = { # Add information to the form to test duplicate email
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': my_user.email,
            'password1': password,
            'password2': password,
        }
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid()) # Should return false since there shouldnt be two users with the same email

    def test_duplicate_user_username(self):
        """
        Test that a user is not able to create an account with the same username as a user that is already created.
        """
        my_user = create_user() # Create the first user
        form_data = { # Add information to the form to test duplicate username
            'first_name': 'John',
            'last_name': 'Doe',
            'username': my_user.username,
            'email': 'johndoe@example.com',
            'password1': password,
            'password2': password,
        }
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid()) # Should return false since there should not be two users with the same username

class UsersViewsTests(TestCase):

    def test_landing_view(self):
        """
        An unauthenticated user will be able to access the landing page.
        """
        response = self.client.get(reverse('landing')) # Landing page should be accessible as a unauthenticated user
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_unable_to_access_unauthenticated_pages(self):
        """
        The user should be not be able to access the unauthenticated pages once they are logged in.
        """
        my_user = create_user() # Create a user
        self.client.login(username=my_user.username, password=password) # Log the user in
        response = self.client.get(reverse('landing')) # Test if the user can reach the unauthenticated pages
        self.assertFalse(response.status_code==200) # They should not be able to
        response = self.client.get(reverse('login'))
        self.assertFalse(response.status_code==200)
        response = self.client.get(reverse('register'))
        self.assertFalse(response.status_code==200)

    def test_login_view(self):
        """
        Test if the user is able to login properly.
        """
        response = self.client.get(reverse('login')) # Make sure the unauthenticated user is able to access it
        self.assertEqual(response.status_code, 200)
        user = create_user() # Create a user to log in
        post = self.client.post(reverse('login'), {'username': user.username, 'password': password}) # Log the user in
        self.assertEqual(post.url, reverse('user_home')) # Should redirect to user home page

    def test_register_view(self):
        response = self.client.get(reverse('register')) # Make sure the unauthenticated user is able to access it
        self.assertEqual(response.status_code, 200)
        post = self.client.post(reverse('register'), { # Create the user using the form
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': password+'#01',
            'password2': password+'#01',
        })
        self.assertEqual(post.url, reverse('login')) # When user is successfully created it redirects to login page
        self.client.login(username='johndoe', password=password+'#01') # Log the user in
        response = self.client.get(reverse('user_home')) # Should be able to access user home if successfully created
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_able_to_access_user_home(self):
        """
        The user should be able to access an the user home once they are logged in.
        """
        my_user = create_user() # Create the user
        self.client.login(username=my_user.username, password=password) # Log the user in
        response = self.client.get(reverse('user_home')) # Try to reach the user home page
        self.assertEqual(response.status_code, 200) # Should be able to reach it

    def test_unauthenticated_user_unable_to_access_user_home(self):
        """
        An unauthenticated user should not be able to access the user home.
        """
        response = self.client.get(reverse('user_home')) # Try to reach the user home page as an unauthenticated user
        self.assertFalse(response.status_code==200) # Should not work

    def test_authenticated_user_able_to_access_user_profile(self):
        """
        The user should be able to access their profile once they are logged in.
        """
        my_user = create_user() # Create the user
        create_profile(user=my_user) # Create the profile for that user
        self.client.login(username=my_user.username, password=password) # Log the user in
        response = self.client.get(reverse('profile')) # Get the profile page for the user
        self.assertEqual(response.status_code, 200) # Should get it successfully
        response = self.client.get(reverse('edit_profile')) # It should also work for the edit profile page
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_unable_to_access_user_profile(self):
        """
        An unauthenticated user should not be able to access the user profile.
        """
        response = self.client.get(reverse('profile')) # Get the profile page
        self.assertFalse(response.status_code==200) # Should redirect since the user is not logged in
        response = self.client.get(reverse('edit_profile')) # It should also apply to the edit profile page
        self.assertFalse(response.status_code==200)

    def test_authenticated_user_able_to_access_user_settings(self):
        """
        The user should be able to access their settings once they are logged in.
        """
        my_user = create_user() # Create the user
        create_profile(user=my_user) # Create their profile
        self.client.login(username=my_user.username, password=password) # Log the user in
        response = self.client.get(reverse('settings')) # Get the settings page for the user
        self.assertEqual(response.status_code, 200) # Should be able to access it
        response = self.client.get(reverse('change_password')) # It should also apply to the change password page
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('change_password')) # It should also apply to the deactivate page
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_unable_to_access_user_settings(self):
        """
        An unauthenticated user should not be able to access the user settings.
        """
        response = self.client.get(reverse('settings')) # Get the settings page
        self.assertFalse(response.status_code==200) # Should redirect since the user is not logged in
        response = self.client.get(reverse('change_password')) # It should also apply to the change password page
        self.assertFalse(response.status_code==200)
        response = self.client.get(reverse('deactivate')) # It should also apply to the deactivate page
        self.assertFalse(response.status_code==200)
