from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_management.views import CreateUserView, LoginUserView, LogoutUserView, ProfileView, UpdateUserView, \
    DeleteUserView


class TestUrlsUserManagement(SimpleTestCase):
    """Test class to check that urls from user-management app retrieve the correct django view"""
    def test_url_register(self):
        url = reverse('user_management:user-register')
        self.assertEquals(resolve(url).func.view_class, CreateUserView)

    def test_url_login(self):
        url = reverse('user_management:user-login')
        self.assertEquals(resolve(url).func.view_class, LoginUserView)

    def test_url_logout(self):
        url = reverse('user_management:user-logout')
        self.assertEquals(resolve(url).func.view_class, LogoutUserView)

    def test_url_user_profile(self):
        url = reverse('user_management:user')
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_url_update_user_profile(self):
        url = reverse('user_management:user-update')
        self.assertEquals(resolve(url).func.view_class, UpdateUserView)

    def test_url_delete_user(self):
        url = reverse('user_management:delete-user')
        self.assertEquals(resolve(url).func.view_class, DeleteUserView)

