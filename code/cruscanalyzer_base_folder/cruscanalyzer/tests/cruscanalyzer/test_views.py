from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from text_management.models import Text, Analysis


class TestViewsTextManagement(TestCase):
    """
    Test class to check correct functioning of base Django views

    It is first tested that the views are not reachable by a not authenticated user, then view functional check
    """
    def setUp(self):
        """
        Set up of a sample test environment with a dummy client that impersonates the user and a sample text
         to process during the test
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.text1 = Text.objects.create(
            user_owner=self.user,
            title="Promessi Sposi",
            author="Alessandro Manzoni",
            link='www.promessi_sposi.com',
            complexity='10'
        )
        Analysis.objects.create(text=self.text1, word='ciao', frequency=2)
        Analysis.objects.create(text=self.text1, word='zio', frequency=3)
        Analysis.objects.create(text=self.text1, word='come', frequency=4)

    def testLogin(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('user_management:user-login'))
        self.assertEqual(response.status_code, 200)

    def test_view_home_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_view_other_user_profile_GET(self):
        response = self.client.get(reverse('other-user', kwargs={'pk': self.user.pk}))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('other-user', kwargs={'pk': self.user.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_info.html')
