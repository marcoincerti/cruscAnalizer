from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.http import urlencode

from lib.text_analysis import ari_complexity_text
from text_management.models import Text


class AcceptanceTest(TestCase):
    def setUp(self):
        """
        Setting up the context for the test.
        """
        self.client = Client()
        # Creating a User
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        # Creating 2 texts (still not saved in the database)
        self.text_1 = Text(pk=1,
                           user_owner=None,
                           title='Promessi Sposi',
                           author='Alessandro Manzoni',
                           link='www.promessi_sposi.com',
                           category=None)
        self.text_1.content = 'Nel mezzo del cammin di nostra vita. Mi ritrovai in una selva oscura!'
        self.text_2 = Text(pk=2,
                           user_owner=self.user,
                           title="Il gatto e la volpe",
                           author="Battiato",
                           link='',
                           category=None)
        self.text_2.content = 'Prova del testo 2 di Battiato.'

    def test_acceptance(self):
        """
        Testing the creation of a user through the manual registration, the inserting of two texts by two different
        users and the comparing of those two texts.
        """
        # Manual registration (POST)
        self.manual_user = {
            'username': 'mike_button',  # Required
            'first_name': 'Mike',  # Optional
            'last_name': 'Button',  # Required
            'email': 'button@gmail.com',
            'password1': 'bangbaing',
            'password2': 'bangbaing',  # Required
        }
        response = self.client.post(reverse('user_management:user-register'), data=self.manual_user, follow=True)
        self.assertRedirects(response, reverse('user_management:user-login'), status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        # Manual login with mike_button
        data_to_send = {
            'username': 'mike_button',  # Required
            'password': 'bangbaing',  # Required
        }
        response = self.client.post(reverse('user_management:user-login'), data=data_to_send, follow=True)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        # text insert for mike_button
        self.manual_user = User.objects.get(username__icontains='mike_button')
        self.text_1.user_owner = self.manual_user
        data_to_send = {
            'user_owner': self.text_1.user_owner,
            'title': self.text_1.title,
            'author': self.text_1.author,
            'link': self.text_1.link,
            'text': self.text_1.content,
        }
        response = self.client.post(reverse('text_management:text-insert'), data=data_to_send)
        self.assertEqual(response.status_code, 200)

        # text-save
        self.text_data_1 = {
            'text_to_save[title]': self.text_1.title,
            'text_to_save[author]': self.text_1.author,
            'text_to_save[link]': self.text_1.link,
            'text_to_save[category]': '',
            'text_to_save[complexity]': ari_complexity_text(self.text_1.content),
            'text_to_save[analysis][ciao]': '2',
            'text_to_save[analysis][amico]': '3',
            'text_to_save[analysis][come]': '4',
            'text_to_save[pk]': self.text_1.pk,
        }
        response = self.client.post(reverse("text_management:save-text-function"),
                                    data=self.text_data_1,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

        # Logging out mike_button and logging in john
        response = self.client.post(reverse('user_management:user-logout'), follow=True)
        self.assertRedirects(response, reverse('user_management:user-login') + '?next=/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.client.login(username='john', password='johnpassword')

        # text insert for john
        data_to_send = urlencode({
            'user_owner': self.text_2.user_owner,
            'title': self.text_2.title,
            'author': self.text_2.author,
            'text': self.text_2.content,
        })
        response = self.client.post(reverse('text_management:text-insert'), None, data_to_send)
        self.assertEqual(response.status_code, 200)

        # text-save
        self.text_data_2 = {
            'text_to_save[title]': self.text_2.title,
            'text_to_save[author]': self.text_2.author,
            'text_to_save[link]': '',
            'text_to_save[category]': '',
            'text_to_save[complexity]': ari_complexity_text(self.text_2.content),
            'text_to_save[analysis][ciao]': '4',
            'text_to_save[analysis][amico]': '3',
            'text_to_save[analysis][come]': '2',
            'text_to_save[pk]': self.text_2.pk,
        }
        response = self.client.post(reverse("text_management:save-text-function"),
                                    data=self.text_data_2,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

        # view saved analysis text_2
        response = self.client.get(reverse("text_management:saved-text-analysis",
                                           kwargs={'pk': self.text_2.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/single_text_analysis.html')

        # text-comparison
        response = self.client.get(reverse("text_management:compare-text-analysis", kwargs={
            'first_pk': self.text_1.pk,
            'second_pk': self.text_2.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/compare_text_analysis.html')

        # text-update, changing the title
        self.assertEquals('Il gatto e la volpe', self.text_2.title)
        response = self.client.post(reverse("text_management:text-update",
                                            kwargs={'pk': self.text_2.pk}), data={'title': 'Titolo modificato.'},
                                    follow=True)
        self.assertRedirects(response, reverse('text_management:saved-text-analysis', kwargs={'pk': self.text_2.pk}),
                             status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.text_2 = Text.objects.get(pk=self.text_2.pk)
        self.assertEquals('Titolo modificato.', self.text_2.title)

        # text-delete
        response = self.client.post(reverse("text_management:text-delete",
                                            kwargs={'pk': self.text_2.pk}), follow=True)
        self.assertRedirects(response, reverse('text_management:text-list'), status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        # text-update not possible when text is owned by a different user
        response = self.client.get(reverse("text_management:text-update",
                                           kwargs={'pk': self.text_1.pk}))
        self.assertEquals(response.status_code, 403)

        # text-delete not possible when text is owned by a different user
        response = self.client.post(reverse("text_management:text-delete",
                                            kwargs={'pk': self.text_1.pk}), follow=True)
        self.assertEquals(response.status_code, 403)

        # Checking the right number of database object, two users and two texts created, one text destroyed
        self.assertEquals(1, Text.objects.count())
        self.assertEquals(2, User.objects.count())
