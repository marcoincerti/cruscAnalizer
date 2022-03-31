from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from text_management.models import Text, Analysis


class TestViewsUserManagement(TestCase):
    """
    Test class to check correct functioning of Django views in User Management app
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

    def test_view_create_user_GET(self):
        response = self.client.get(reverse('user_management:user-register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration_form.html')

    def test_view_login_user_GET(self):
        response = self.client.get(reverse('user_management:user-login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_view_logout_user_GET(self):
        response = self.client.get(reverse('user_management:user-logout'))
        self.assertEquals(response.status_code, 302)  # Check sul redirect a home

    def test_view_user_profile_GET(self):
        response = self.client.get(reverse('user_management:user'))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('user_management:user'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/user_profile.html')

    def test_view_edit_user_profile_GET(self):
        response = self.client.get(reverse('user_management:user-update'))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('user_management:user-update'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/user_update.html')

    def test_view_delete_user(self):
        response = self.client.get(reverse('user_management:delete-user'))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('user_management:delete-user'))
        self.assertEquals(response.status_code, 302)
        # Testing if the user is deleted, and also if all his texts and analysis are deleted from the DB.
        self.assertEquals(User.objects.filter(pk=self.user.pk).count(), 0)
        self.assertEquals(Text.objects.filter(pk=self.user.pk).count(), 0)
        self.assertEquals(Analysis.objects.filter(text__in=self.user.user_texts.all()).count(), 0)
