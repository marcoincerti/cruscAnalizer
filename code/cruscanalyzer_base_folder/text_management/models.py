import copy

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from lib.text_analysis import analyze_text


class Category(models.Model):
    """
    Model to store the possible categories of a text.
    They are pre-inserted by the admins of the project and are not modifiable by the users.
    """
    name = models.CharField(max_length=150)

    def __repr__(self):
        return self.name

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class Text(models.Model):
    """
    Model to store the metadata of a text.
    """
    user_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='user_texts')  # Reference to the table User, created automatically by
    # Django authentication system.
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150, null=True, blank=True)
    link = models.URLField(max_length=250, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='category_texts')  # If the text category is cancelled, it is set as NULL.
    complexity = models.DecimalField(max_digits=20, decimal_places=2)

    content = ""  # Text content, not stored because of copyright problems
    _analysis = None  # Analysis of the text

    @property
    def analysis(self):
        """
        Property called when trying to access mytext.analysis, calculates the analysis with the the Models Analysis of
        this text if stored, otherwise calculates it with the function analyze_text with the text content.
        :returns: dict containing the words and their frequency in descending order
        """
        if self._analysis is None:
            if self.content == "":
                self._analysis = {}
                # Sets up the dictionary of the text_analysis
                for query_result in Analysis.objects.filter(text_id=self.pk):
                    self._analysis[query_result.word] = query_result.frequency
            else:
                self._analysis = dict(analyze_text(self.content)
                                      .most_common())  # Calculate and store the analysis of the text
        return self._analysis

    @property
    def word_counter(self):
        """
        Property called when trying to access mytext.word_counter, calculates the total number of words of the text.
        :returns: total number of words of the text saved in the database.
        """
        return Analysis.objects.filter(text_id=self.pk).count()

    def filtered_analysis(self, user):
        """
        Filters the text analysis with the words inside the user blacklist.
        :param user: Used to get the words of his blacklist.
        :returns: the filtered analysis without the "blackwords".
        """
        filtered_analysis = copy.deepcopy(self.analysis)  # Deepcopy to avoid changing the original dict.
        for black_word in user.user_text_settings.blacklist:
            filtered_analysis.pop(black_word, None)
        return filtered_analysis

    def get_black_words_number(self, user):
        """
            Counts how many black words are present in an analysis of a text.
            :param user: Used to get the words of his blacklist.
            :return black_words_number: number of black words in the text.
        """
        black_words_number = 0
        for black_word in user.user_text_settings.blacklist:
            if black_word in self.analysis:
                black_words_number += 1
        return black_words_number

    def remove_short_words_from_analysis(self, min_characters):
        """
        Removes from the text analysis the words that are shorter than min_characters.
        :param min_characters: int of the minimum number of characters that a word has to have in order to be saved.
        """
        self._analysis = {word: freq for word, freq in self.analysis.items() if len(word) >= min_characters}

    def to_dict_only_metadata(self):
        """
        Function called from the javascript script when using filter json_script, in order to access safely the text data
        :return: dictionary with the object data
        """
        return {'title': self.title,
                'author': self.author,
                'link': self.link,
                'category': self.category.pk if self.category else None,
                'complexity': self.complexity,
                'analysis': self.analysis,
                }

    def __repr__(self):
        return '"%s", by %s.' % (self.title, self.author)

    class Meta:
        ordering = ['-pk', ]  # Ordering for DESC pk (last inserted first)


class Analysis(models.Model):
    """
    Model to store the analysis of a text.
    Fields: - Reference to the original text.
            - Word of the text.
            - Frequency of the word inside the text.
    """
    text = models.ForeignKey(Text, on_delete=models.CASCADE, related_name='text_analysis')
    word = models.CharField(max_length=40)
    frequency = models.IntegerField()

    def __repr__(self):
        return '"%s" -> %s times.' % (self.word, self.frequency)

    class Meta:
        ordering = ['text__pk', '-frequency', ]  # Ordering for ASC text and DESC frequency


class UserTextSettings(models.Model):
    """
    Model to store the custom text settings of a user.
    Fields: - Reference to the user.
            - His blacklist (words not to be displayed by the analyzes) --> String with words separated by ;
            - Minimum number of characters the words must have, otherwise they're not saved in the analyzes.
    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='user_text_settings')
    blacklist_string = models.TextField(default='')
    min_characters = models.IntegerField(default=0)

    @property
    def blacklist(self):
        """
        Property that removes all the whitespaces from the stored blacklist and returns the words in it that are
        separated by a ; as a list
        :returns: list of words of the blacklist
        """
        if self.blacklist_string == '':
            return []
        return (''.join(self.blacklist_string.split())).split(';')


@receiver(post_save, sender=User)
def create_favorites(sender, instance, created, **kwargs):
    """
    When a new :User: is created, it creates his UserTextSettings
    :param sender:
    :param instance: of the user created
    :param created: bool
    :param kwargs:
    :returns:
    """
    if created:
        UserTextSettings.objects.create(user=instance)
