import decimal
import unittest
from collections import Counter

from django import test
from django.contrib.auth.models import User
from django.db.models import Avg

from lib.text_analysis import analyze_text, ari_complexity_text
from lib.text_translation import translate, get_languages
from lib.text_statistics import get_avg_complexity, get_count_text
from googletrans import LANGUAGES

from text_management.models import Text


class TestTokenize(unittest.TestCase):
    """
    Tests for the function that analyses a text.
    """
    def setUp(self):
        self.source_text = "una povera lepre che si vantava di correre più veloce di un' altra povera lepre"
        self.source_text_insensitive = "UnA povEra lEprE chE si VaNtava di coRRere più vELoce Di un' alTRA poveRA lEPRE"
        self.tester = Counter(
            {'una': 1, 'povera': 2, 'lepre': 2, 'che': 1, 'si': 1, 'vantava': 1, 'di': 2, 'correre': 1, 'più': 1,
             'veloce': 1,
             'un': 1, 'altra': 1})

    def test_number_of_occurences(self):
        self.assertEqual(analyze_text(self.source_text), self.tester)

    def test_no_text(self):
        self.assertEqual(analyze_text(""), Counter({}))

    def test_case_insensitive(self):
        self.assertEqual(analyze_text(self.source_text_insensitive), self.tester)

    def test_wrong_input_type(self):
        self.assertRaises(TypeError, analyze_text, 1)


class TestComplexityCalculator(unittest.TestCase):
    """
    Tests for the function that calculates the ARI complexity of a text.
    """
    def setUp(self):
        self.source_text = "una povera lepre che si vantava di correre più veloce di un' altra povera lepre"

    def test_wrong_input_type(self):
        self.assertRaises(TypeError, ari_complexity_text, 1)

    def test_value_returned(self):
        self.assertEqual(ari_complexity_text(self.source_text), 10.88)

    def test_source_input_empty(self):
        self.assertEqual(ari_complexity_text(""), None)

    def test_source_input_1_char(self):
        self.assertEqual(ari_complexity_text("H"), 0)


class TestTranslate(unittest.TestCase):
    """
    Tests for the functions of translation with Google Translate API.
    """
    def test_wrong_input_type(self):
        self.assertRaises(TypeError, translate, 1)

    def test_value_returned(self):
        self.assertEqual(translate("Casa", "it", "en"), "Home")

    def test_languages_returned(self):
        self.assertEqual(get_languages(), LANGUAGES)


class TestStatistics(test.TestCase):
    def setUp(self):
        """Set up of 3 sample text to use to check database functionality"""
        self.user = User.objects.create()
        self.text_list = [Text.objects.create(
            user_owner=self.user,
            title="Promessi Sposi",
            author="Alessandro Manzoni",
            link='www.promessi_sposi.com',
            complexity=10.74),
            Text.objects.create(
                user_owner=self.user,
                title="After Hours",
                author="The Weeknd",
                complexity=15.23),
            Text.objects.create(
                user_owner=self.user,
                title="Ignorance",
                complexity=33.52),
        ]
        for text in self.text_list:
            text.save()

    def test_avg_complexity(self):
        """
        Tests for the function of calculating the average complexity of a sets of Texts (model).

        :returns: Passed if the return value of the function is the same as the average value calculated directly on the
        database and locally with python sum(complexities)/len of the texts.
        """
        text_saved = Text.objects.filter(user_owner=self.user)
        complexity = round(decimal.Decimal(sum([text.complexity for text in self.text_list]) /
                                           len(self.text_list)), 2)
        self.assertEqual(get_avg_complexity(text_saved), text_saved.aggregate(Avg('complexity'))['complexity__avg'])
        self.assertEqual(get_avg_complexity(text_saved), complexity)

    def test_count_texts(self):
        """
        Tests for the function of calculating the number of a sets of Texts (model).

        :returns: Number of texts
        """
        text_saved = Text.objects.filter(user_owner=self.user)

        self.assertEqual(get_count_text(text_saved), 3)
