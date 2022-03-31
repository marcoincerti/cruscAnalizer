from django.contrib.auth.models import User
from django.test import TestCase, Client

from text_management.models import Text, Analysis
from text_management.templatetags.app_filters import get_ordered_words_frequencies_blacklist_filtered


class TestTemplateTags(TestCase):
    """
    Test class to check correct functioning of template tags.

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
        Analysis.objects.create(text=self.text2, word='progetto', frequency=1)

    def test_get_user_popular_words(self):
        """
        Tests if the popular words of the user are filtered with the blacklist of the authenticated user
        """
        self.user.user_text_settings.blacklist_string = 'prova; covid'
        self.assertEquals(get_ordered_words_frequencies_blacklist_filtered(self.user.user_texts.all(), self.user),
                          [('weeknd', 15), ('come', 4), ('zio', 3), ('ciao', 2), ('progetto', 1)])
