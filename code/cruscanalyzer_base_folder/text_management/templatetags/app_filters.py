from statistics import mean

from django.template.defaulttags import register
from lib import text_statistics

"""
Templates don't support some functions on the variables. Those are some personalized filter.
"""


@register.filter
def get_item(dictionary, key):
    """
    Filter to get the value of a specific key of a dictionary.
    """
    return dictionary.get(key)


@register.filter
def get_dict_items(dictionary):
    """
    Filter to get the items of a dictionary.
    """
    return dictionary.items()


@register.filter
def get_avg_complexity(texts):
    """
    Filter to be used inside templates to get the average complexity of a set of texts.
    :param texts: Set of models "Text".
    :returns: Average complexity as float with 2 decimals after.
    """
    return text_statistics.get_avg_complexity(texts)


@register.filter
def get_count_texts(texts):
    """
    Filter to be used inside templates to get number of texts.
    :param texts: Set of models "Text".
    :returns: Number of texts.
    """
    return text_statistics.get_count_text(texts)


@register.filter
def get_user_words(texts):
    """
       Filter to be used inside templates to get number of words in the texts.
       :param texts: Set of models "Text".
       :returns: Number of words in the list of texts.
    """
    return text_statistics.get_count_words(texts)


@register.filter
def get_ordered_words_frequencies_blacklist_filtered(texts, user):
    """
       Filter to be used inside templates to get all analysis words of the texts ordered by frequency.
       :param user: Filters the popular words of the user with his blacklist.
       :param texts: Set of models "Text".
       :returns: Five top frequency words.
    """
    # Lambda function to filter only the tuples where the key (word) is not in the user blacklist
    ordered_words_frequency = list(filter(lambda tuple_word_freq: tuple_word_freq[0] not in user.user_text_settings
                                          .blacklist, text_statistics.get_ordered_words_frequencies(texts)))
    return ordered_words_frequency


@register.filter
def get_user_complexity_plot(texts):
    """
    Filter to be used inside templates to get complexity of the texts.
    :param texts: Set of models "Text".
    :returns: Complexity of the texts.
    """
    return text_statistics.get_complexity(texts)


@register.filter
def get_filtered_analysis(text, user):
    """
    Filter to be used inside templates to get the filtered analysis of a text (without words in user blacklist).
    :param text: to show the filtered analysis of.
    :param user: Filter the analysis with the words inside his blacklist.
    :returns: Filtered analysis.
    """
    return text.filtered_analysis(user)


@register.filter
def get_avg_complexity_all_users(users):
    """
    Filter to be used inside templates to get the average complexity of all texts.
    :param users: Filter the analysis with the words inside his blacklist.
    :returns: Filtered analysis.
    """
    return text_statistics.get_avg_complexity_all_users(users)


@register.filter
def get_avg_frequency(obj):
    """
    Filter that calculate the average frequency of a given object.
    :param obj: the object that contains words and frequencies.
    :return: the average frequency of the object.
    """
    if len(obj) == 0:
        return 0
    if isinstance(obj, dict):
        return mean(obj.values())
    elif isinstance(obj, list):
        return mean([freq for (word, freq) in obj])
    elif isinstance(obj, int):
        return object
    else:
        return 0


@register.filter
def get_obj_len(obj):
    """
    Filter that calculate the length of a given object.
    :param obj: the object whose length we want to calculate.
    :return: the length of the object.
    """
    if len(obj) == 0:
        return 0
    if isinstance(obj, dict):
        return len(obj.keys())
    elif isinstance(obj, list):
        return len(obj)
    elif isinstance(obj, int):
        return object
    else:
        return 0


@register.filter
def get_texts_by_category(texts):
    """
    Gets how many texts are present in each category.
    :param texts: Set of models "Text".
    :return: how many texts are present in each category.
    """
    return text_statistics.get_texts_by_category(texts)


@register.filter
def get_hidden_words_number(text, user):
    """
    Gets how many words have been hidden by blacklist in a text.
    :param text: Instance of model "Text".
    :param user: Filter the analysis with the words inside his blacklist.
    :return: how many words have been hidden in the text.
    """
    return text.get_black_words_number(user)
