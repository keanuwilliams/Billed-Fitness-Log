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
        user = create_user()
        profile = create_profile(user=user)
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(user.profile, profile)
        self.assertEqual(profile.__str__(), f'{user.username} Profile')

class UserTests(TestCase):

    def test_register_user(self):
        """
        Test that a user is able to create an account properly by checking if the user is in the database after the account is created.
        """
        my_user = create_user()
        my_user_from_database = User.objects.get(username="myuser")
        self.assertEqual(my_user, my_user_from_database)
        self.assertTrue(my_user.is_active)
        self.assertFalse(my_user.is_staff)
        self.assertFalse(my_user.is_superuser)

    def test_duplicate_user_email(self):
        """
        Test that a user is not able to create an account with the same email as a user that is already created.
        """
        my_user = create_user()
        try:
            my_second_user = create_user(first_name='John', last_name="Doe", username="johndoe")
        except Exception as e:
            pass # if exception is raised, that is a good sign
        else:
            self.assertNotEqual(my_user.email, my_second_user.email)

    def test_duplicate_user_username(self):
        """
        Test that a user is not able to create an account with the same username as a user that is already created.
        """
        my_user = create_user()
        try:
            my_second_user = create_user(first_name='John', last_name="Doe", email="johndoe@example.com")
        except Exception as e:
            pass # if exception is raised, that is a good sign
        else:
            self.assertNotEqual(my_user.username, my_second_user.username)


class UsersViewsTests(TestCase):

    def test_landing_view(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_unable_to_access_unauthenticated_pages(self):
        """
        The user should be not be able to access the unauthenticated pages once they are logged in.
        """
        my_user = create_user()
        self.client.login(username=my_user.username, password=password)
        response = self.client.get(reverse('landing'))
        self.assertIs(response.status_code==200, False)
        response = self.client.get(reverse('login'))
        self.assertIs(response.status_code==200, False)
        response = self.client.get(reverse('register'))
        self.assertIs(response.status_code==200, False)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        user = create_user()
        post = self.client.post(reverse('login'), {'username': user.username, 'password': password})
        self.assertEqual(post.url, '/home/')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        # Add more to the register page

    def test_authenticated_user_able_to_access_user_home(self):
        """
        The user should be able to access an the user home once they are logged in.
        """
        response = self.client.get(reverse('login'))
        my_user = create_user()
        self.client.login(username=my_user.username, password=password)
        response = self.client.get(reverse('user_home'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_unable_to_access_user_home(self):
        """
        An unauthenticated user should not be able to access the user home.
        """
        response = self.client.get(reverse('user_home'))
        self.assertEqual(response.status_code==200, False)

    def test_authenticated_user_able_to_access_user_profile(self):
        """
        The user should be able to access their profile once they are logged in.
        """
        response = self.client.get(reverse('login'))
        my_user = create_user()
        create_profile(user=my_user)
        self.client.login(username=my_user.username, password=password)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_unable_to_access_user_profile(self):
        """
        An unauthenticated user should not be able to access the user profile.
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code==200, False)
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code==200, False)
