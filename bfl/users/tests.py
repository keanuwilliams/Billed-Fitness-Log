from django.test import TestCase
from django.urls import reverse
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User

password = 'mypassword'  # Global password to be used in tests


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
        # Create the user
        user = create_user()
        # Create the profile for the user
        profile = create_profile(user=user)
        # Make sure the profile is an instance of Profile
        self.assertTrue(isinstance(profile, Profile))
        # Make sure that the profile is associated to the user
        self.assertEqual(user.profile, profile)
        # Make sure that the profile prints correctly
        self.assertEqual(profile.__str__(), f'{user.username} Profile')

    def test_user_default_picture(self):
        """
        When a user creates an account and profile, the default profile picture should be "default.jpeg".
        """
        # Create the user
        user = create_user()
        # Create the profile for the user
        create_profile(user=user)
        # Make sure the default profile picture is the default.jpeg
        self.assertEqual(user.profile.image.url, "/media/default.jpeg")


class UserCreationTests(TestCase):

    def test_register_user(self):
        """
        Test that a user is able to create an account properly by checking if the user is in the database after the
        account is created.
        """
        # Create a user
        my_user = create_user()
        # Grab from the database the user
        my_user_from_database = User.objects.get(username="myuser")
        # Compare the users to see if they are the same
        self.assertEqual(my_user, my_user_from_database)
        # Make sure when user is created they are equal
        self.assertTrue(my_user.is_active)
        # Make sure that the user does not have admin status
        self.assertFalse(my_user.is_staff)
        self.assertFalse(my_user.is_superuser)

    def test_duplicate_user_username(self):
        """
        Test that a user is not able to create an account with the same username as a user that is already created.
        """
        # Create an initial user
        my_user = create_user()
        try:
            # Create a duplicate user with the same username
            my_second_user = create_user(first_name='John', last_name="Doe", email="johndoe@example.com")
        except User.DoesNotExist:
            # if exception is raised, that is a good sign
            pass
        else:
            # Check if the usernames for both of the users are equal if an error isn't raised
            self.assertNotEqual(my_user.username, my_second_user.username)


class UserRegisterFormTests(TestCase):

    def test_duplicate_user_email(self):
        """
        Test that a user is not able to create an account with the same email as a user that is already created.
        """
        # Create the first user
        my_user = create_user()
        # Add information to the form to test duplicate email
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': my_user.email,
            'password1': password,
            'password2': password,
        }
        form = UserRegisterForm(data=form_data)
        # Should return false since there shouldn't be two users with the same email
        self.assertFalse(form.is_valid())

    def test_duplicate_user_username(self):
        """
        Test that a user is not able to create an account with the same username as a user that is already created.
        """
        # Create the first user
        my_user = create_user()
        # Add information to the form to test duplicate email
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': my_user.username,
            'email': 'johndoe@example.com',
            'password1': password,
            'password2': password,
        }
        form = UserRegisterForm(data=form_data)
        # Should return false since there shouldn't be two users with the same email
        self.assertFalse(form.is_valid())


class UserUpdateFormTests(TestCase):

    def test_duplicate_user_email(self):
        """
        Test that a user is not able to create an account with the same email as a user that is already created.
        """
        # Create the first user
        my_user = create_user()
        # Add information to the form to test duplicate email
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': my_user.email,
            'password1': password,
            'password2': password,
        }
        form = UserUpdateForm(data=form_data)
        # Should return false since there shouldn't be two users with the same email
        self.assertFalse(form.is_valid())

    def test_duplicate_user_username(self):
        """
        Test that a user is not able to create an account with the same username as a user that is already created.
        """
        # Create the first user
        my_user = create_user()
        # Add information to the form to test duplicate username
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': my_user.username,
            'email': 'johndoe@example.com',
            'password1': password,
            'password2': password,
        }
        form = UserUpdateForm(data=form_data)
        # Should return false since there should not be two users with the same username
        self.assertFalse(form.is_valid())


class UsersViewsTests(TestCase):

    def test_landing_view(self):
        """
        An unauthenticated user will be able to access the landing page.
        """
        # Landing page should be accessible as a unauthenticated user
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_unable_to_access_unauthenticated_pages(self):
        """
        The user should be not be able to access the unauthenticated pages once they are logged in.
        """
        # Create a user
        my_user = create_user()
        # Log the user in
        self.client.login(username=my_user.username, password=password)
        # Test if the user can reach the unauthenticated pages
        response = self.client.get(reverse('landing'))
        self.assertFalse(response.status_code == 200)
        response = self.client.get(reverse('login'))
        self.assertFalse(response.status_code == 200)
        response = self.client.get(reverse('register'))
        self.assertFalse(response.status_code == 200)

    def test_login_view(self):
        """
        Test if the user is able to login properly.
        """
        # Make sure the unauthenticated user is able to access it
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        # Create a user to log in
        user = create_user()
        # Log the user in
        post = self.client.post(reverse('login'), {'username': user.username, 'password': password})
        # Should redirect to user home page
        self.assertEqual(post.url, reverse('user-home'))

    def test_register_view(self):
        # Make sure the unauthenticated user is able to access it
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        # Create the user using the form
        post = self.client.post(reverse('register'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': password+'#01',
            'password2': password+'#01',
        })
        # When user is successfully created it redirects to login page
        self.assertEqual(post.url, reverse('login'))
        # Log the user in
        self.client.login(username='johndoe', password=password+'#01')
        # Should be able to access user home if successfully created
        response = self.client.get(reverse('user-home'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_able_to_access_user_home(self):
        """
        The user should be able to access an the user home once they are logged in.
        """
        # Create the user
        my_user = create_user()
        # Log the user in
        self.client.login(username=my_user.username, password=password)
        # Try to reach the user home page
        response = self.client.get(reverse('user-home'))
        # Should be able to reach it
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_unable_to_access_user_home(self):
        """
        An unauthenticated user should not be able to access the user home.
        """
        # Try to reach the user home page as an unauthenticated user
        response = self.client.get(reverse('user-home'))
        # Should not work
        self.assertFalse(response.status_code == 200)

    def test_authenticated_user_able_to_access_user_profile(self):
        """
        The user should be able to access their profile once they are logged in.
        """
        # Create the user
        my_user = create_user()
        # Create the profile for that user
        create_profile(user=my_user)
        # Log the user in
        self.client.login(username=my_user.username, password=password)
        # Get the profile page for the user
        response = self.client.get(reverse('profile', kwargs={'username': my_user.username}))
        # Should get it successfully
        self.assertEqual(response.status_code, 200)
        # It should also work for the edit profile page
        response = self.client.get(reverse('edit-profile', kwargs={'username': my_user.username}))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_unable_to_access_user_profile(self):
        """
        An unauthenticated user should not be able to access the user profile.
        """
        # Create a user and profile to test an unauthenticated user trying to access the user's profile
        my_user = create_user()
        create_profile(user=my_user)
        # Get the profile page
        response = self.client.get(reverse('profile', kwargs={'username': my_user.username}))
        # Should redirect since the user is not logged in
        self.assertFalse(response.status_code == 200)
        # It should also apply to the edit profile page
        response = self.client.get(reverse('edit-profile', kwargs={'username': my_user.username}))
        self.assertFalse(response.status_code == 200)

    def test_authenticated_user_able_to_access_user_settings(self):
        """
        The user should be able to access their settings once they are logged in.
        """
        # Create the user
        my_user = create_user()
        # Create their profile
        create_profile(user=my_user)
        # Log the user in
        self.client.login(username=my_user.username, password=password)
        # Get the settings page for the user
        response = self.client.get(reverse('settings'))
        # Should be able to access it
        self.assertEqual(response.status_code, 200)
        # It should also apply to the change password page
        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 200)
        # It should also apply to the deactivate page
        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_unable_to_access_user_settings(self):
        """
        An unauthenticated user should not be able to access the user settings.
        """
        # Get the settings page
        response = self.client.get(reverse('settings'))
        # Should redirect since the user is not logged in
        self.assertFalse(response.status_code == 200)
        # It should also apply to the change password page
        response = self.client.get(reverse('change-password'))
        self.assertFalse(response.status_code == 200)
        # It should also apply to the deactivate page
        response = self.client.get(reverse('deactivate'))
        self.assertFalse(response.status_code == 200)
