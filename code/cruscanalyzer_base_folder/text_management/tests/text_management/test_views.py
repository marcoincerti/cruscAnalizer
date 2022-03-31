from django.contrib.auth.models import User
from django.template import RequestContext
from django.test import TestCase, Client
from django.urls import reverse
from text_management.models import Text, Analysis, UserTextSettings


class TestViewsTextManagement(TestCase):
    """
    Test class to check correct functioning of Django views in Text Management app

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
        self.text2 = Text.objects.create(
            user_owner=self.user,
            title="Help",
            author="Conte",
            complexity='22.4'
        )
        Analysis.objects.create(text=self.text2, word='prova', frequency=12)
        Analysis.objects.create(text=self.text2, word='weeknd', frequency=15)
        Analysis.objects.create(text=self.text2, word='covid', frequency=30)

    def testLogin(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('user_management:user-login'))
        self.assertEqual(response.status_code, 200)

    def test_view_text_insert_GET(self):
        response = self.client.get(reverse('text_management:text-insert'))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('text_management:text-insert'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/text_insert.html')

    def test_view_text_analysis_POST(self):
        data = {
            'title': 'Prova',
            'author': '',
            'link': '',
            'category': '',
            'text': 'Prova di un testo qualunque con testo.',
            'delete_short_words': 'on'
        }
        response = self.client.post(reverse("text_management:text-analysis"), data=data)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse("text_management:text-analysis"), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/single_text_analysis.html')

    def test_view_text_analysis_saved_GET(self):
        response = self.client.get(reverse("text_management:saved-text-analysis", kwargs={'pk': self.text1.pk}))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:saved-text-analysis", kwargs={'pk': self.text1.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/single_text_analysis.html')

    def test_view_list_texts_user_GET(self):
        response = self.client.get(reverse("text_management:text-list"))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:text-list"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/user_text_list.html')

    def test_view_search_GET(self):
        response = self.client.get(reverse("text_management:text-search"))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:text-search"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/search_list.html')

    def test_view_delete_text_GET(self):
        response = self.client.get(reverse("text_management:text-delete", kwargs={'pk': self.text1.pk}))
        self.assertEquals(response.status_code, 403)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:text-delete", kwargs={'pk': self.text1.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/text_delete.html')

    def test_view_update_text_GET(self):
        response = self.client.get(reverse("text_management:text-update", kwargs={'pk': self.text1.pk}))
        self.assertEquals(response.status_code, 403)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:text-update", kwargs={'pk': self.text1.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/text_update.html')

    def test_view_compare_texts_GET(self):
        response = self.client.get(reverse("text_management:compare-text-analysis", kwargs={
            'first_pk': self.text1.pk, 'second_pk': self.text2.pk}))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:compare-text-analysis", kwargs={
            'first_pk': self.text1.pk, 'second_pk': self.text2.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/compare_text_analysis.html')

    def test_view_dashboard_GET(self):
        response = self.client.get(reverse("text_management:dashboard"))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:dashboard"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/dashboard_analytics.html')

    def test_view_user_text_settings_GET(self):
        response = self.client.get(reverse("text_management:text-settings"))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:text-settings"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/text_settings.html')

    def test_view_user_text_settings_POST(self):
        data = {
            'black-word': ['ciao', 'prova'],
            'min-characters': 5,
        }
        response = self.client.post(reverse("text_management:text-settings"), data=data)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse("text_management:text-settings"), data=data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(UserTextSettings.objects.get(user=self.user).blacklist_string, 'ciao;prova')
        self.assertEquals(UserTextSettings.objects.get(user=self.user).blacklist, data['black-word'])
        self.assertEquals(UserTextSettings.objects.get(user=self.user).min_characters, data['min-characters'])

    def test_view_saved_text_analysis_filtering_black_words(self):
        """
        Checks if the words showed in the template are filtrated with the user blacklist.
        """
        response = self.client.get(reverse("text_management:saved-text-analysis", kwargs={'pk': self.text1.pk}))
        self.assertEquals(response.status_code, 302)
        UserTextSettings.objects.filter(user=self.user).update(blacklist_string='ciao;   zio')
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:saved-text-analysis", kwargs={'pk': self.text1.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/single_text_analysis.html')
        self.assertEquals(list(response.context['items']), [('come', 4)])
        UserTextSettings.objects.filter(user=self.user).update(blacklist_string='')

    def test_view_text_analysis_deleting_short_words(self):
        """
        Checks if the words of an inserted text that are too short for the user are deleted and are not showed in the
        template.
        """
        data = {
            'title': 'Prova',
            'author': '',
            'link': '',
            'category': '',
            'text': 'Prova di un testo qualunque con testo.',
            'delete_short_words': 'on'
        }
        response = self.client.post(reverse("text_management:text-analysis"), data=data)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        UserTextSettings.objects.filter(user=self.user).update(min_characters=4)
        response = self.client.post(reverse("text_management:text-analysis"), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_management/single_text_analysis.html')
        self.assertIsInstance(response.context['text_data'], Text)
        response.context['text_data'].remove_short_words_from_analysis(self.user.user_text_settings.min_characters)
        self.assertEquals({
            'prova': 1,
            'testo': 2,
            'qualunque': 1,
        }, response.context['text_data'].analysis)
        self.assertEquals({
            'prova': 1,
            'testo': 2,
            'qualunque': 1,
        }, dict(response.context['items']))
        UserTextSettings.objects.filter(user=self.user).update(min_characters=0)


class TestViewsAjaxTextManagement(TestCase):
    """
    Class for testing the ajax functions.
    The first thing tested is always connecting to the view without being authenticated.
    """
    def setUp(self):
        """
        Setting up the objects used during the tests
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_view_save_text_function_POST(self):
        """
        Testing the ajax function that saves a text.
        The function is reachable only through POST. Created custom test data.
        :returns: True if the response of the page is correct (302 if user not authenticated, 200 if authenticated)
        """
        text_data = {
                        'text_to_save[title]': 'Prova',
                        'text_to_save[author]': 'Tester',
                        'text_to_save[link]': '',
                        'text_to_save[category]': '',
                        'text_to_save[complexity]': '3.40',
                        'text_to_save[analysis][ciao]': '2',
                        'text_to_save[analysis][zio]': '3',
                        'text_to_save[analysis][come]': '4',
                    }
        response = self.client.post(reverse("text_management:save-text-function"),
                                    data=text_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse("text_management:save-text-function"),
                                    data=text_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_view_translate_word_function_GET(self):
        """
        Testing the ajax function that saves a text.
        Created custom data for the tested translation.
        :return: True if the response of the page is correct (302 if user not authenticated, 200 if authenticated)
        :return: True if the translation of the data is correct ("come", from english to italian, is "venire")
        """
        response = self.client.get(reverse("text_management:translate-word"),
                                   data={
                                       'original_word': 'come',
                                       'source_language': 'en',
                                       'dest_language': 'it',
                                       'detect_language': 'false',
                                   },
                                   content_type='application/json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("text_management:translate-word"),
                                   data={
                                       'original_word': 'come',
                                       'source_language': 'en',
                                       'dest_language': 'it',
                                       'detect_language': 'false',
                                   },
                                   content_type='application/json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)  # Check se richiesta funzione corretta
        self.assertIn(b'venire', response.content)  # Check se risultato richiesta è corretto (formato byte)


