from django.test import SimpleTestCase
from django.urls import reverse, resolve

from cruscanalyzer.views import HomePageView, UserProfileView


class TestUrls(SimpleTestCase):
    """Test class to check that base urls retrieve the correct django template"""
    def test_home_is_resolved(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func.view_class, HomePageView)

    def test_other_user_profile_is_resolved(self):
        url = reverse("other-user", kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, UserProfileView)
