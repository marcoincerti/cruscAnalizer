from django.test import TestCase
from text_management.models import Text, Category, Analysis
from django.contrib.auth.models import User


class TestModels(TestCase):
    """Testclass for models and database functionality."""

    def setUp(self):
        """Set up of a sample text to use to check database functionality"""
        user = User.objects.create()
        user.username = "Mario"
        self.text1 = Text.objects.create(
            user_owner=user,
            title="Promessi Sposi",
            author="Alessandro Manzoni",
            link='www.promessi_sposi.com',
            complexity='10'
        )
        Analysis.objects.create(text=self.text1, word='ciao', frequency=2)
        Analysis.objects.create(text=self.text1, word='zio', frequency=3)
        Analysis.objects.create(text=self.text1, word='come', frequency=4)

    def test_title(self):
        self.assertEquals(self.text1.title, "Promessi Sposi")

    def test_author(self):
        self.assertEquals(self.text1.author, "Alessandro Manzoni")

    def test_link(self):
        self.assertEquals(self.text1.link, "www.promessi_sposi.com")

    def test_complexity(self):
        self.assertEquals(self.text1.complexity, "10")

    def test_deletion(self):
        text_id = self.text1.id
        # verify that the actual number of objects is three:
        self.assertEquals(Analysis.objects.filter(text=text_id).count(), 3)
        Text.objects.filter(id=text_id).delete()
        # verify that the objects doesn't exist anymore in the database:
        self.assertRaises(Text.DoesNotExist, Text.objects.get, pk=text_id)
        # verify that the actual number of objects is zero, because of the cascade deletion:
        self.assertEquals(Analysis.objects.filter(text=text_id).count(), 0)

    def test_update(self):
        text_id = self.text1.id
        # verify that the actual title is Promessi Sposi:
        # Text.objects.filter(id=text_id).values_list('title', flat=True)[0]:
        # Return a list of elements (one element for every row), we get the first element with - [0] - (the title)
        self.assertEquals(Text.objects.filter(id=text_id).values_list('title', flat=True)[0], "Promessi Sposi")
        Text.objects.filter(id=text_id).update(title='Promessi Fidanzati')
        # verify that the objects doesn't have the old title anymore:
        self.assertEquals(Text.objects.filter(id=text_id).values_list('title', flat=True)[0], "Promessi Fidanzati")
