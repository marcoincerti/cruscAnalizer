from collections import Counter
from django.db.models import Avg
from text_management.models import Text, Category


def get_avg_complexity(texts):
    """
    Calculates the average complexity of the passed texts.

    :param texts: List of models "Text"
    :returns: float with 2 decimals after .
    """
    if texts is None or len(texts) == 0:
        return 0
    avg_complexity = texts.aggregate(Avg('complexity'))['complexity__avg']  # Aggregate returns a dict.
    return round(avg_complexity, 2)


def get_complexity(texts):
    """
    Select all the values of complexity
    :param texts: List of models "Text".
    :returns: Complexity of the texts.
    """
    dd = []
    if texts is None or len(texts) == 0:
        return 0
    for t in texts:
        dd.append(int(t.complexity))

    return dd[::-1]  # reverse list


def get_count_text(texts):
    """
    Counts how many texts are there.
    :param texts: List of models "Text".
    :returns: Number of texts.
    """
    if texts is None:
        return 0
    return len(texts)


def get_count_words(texts):
    """
    Counts how many words are in the texts.
    :param texts: List of models "Text".
    :returns: Number of words in the list of texts.
    """
    words = 0
    for t in texts:
        words += t.word_counter
    return words


def get_ordered_words_frequencies(texts):
    """
    Gets the words of the texts ordered by descending frequency
    :param texts: List of models "Text".
    :returns: Five more frequent words.
     """
    all_words_frequency = []
    for t in texts:
        analysis = t.analysis
        all_words_frequency.append(analysis)

    ordered_words_frequency = sum((Counter(dict(x)) for x in all_words_frequency), Counter()).most_common()

    return ordered_words_frequency  # list of tuples -> (word, freq)


def get_all_words_frequency(texts):
    """
    Return all words and frequencies in all texts present.
    :param texts: List of models "Text".
    :returns: All words and frequencies.
     """
    all_words_frequency = []
    for t in texts:
        analysis = t.analysis
        all_words_frequency.append(analysis)

    ordered_words_frequency = sum((Counter(dict(x)) for x in all_words_frequency), Counter())
    ordered_words_frequency = ordered_words_frequency.most_common()

    return ordered_words_frequency  # list of tuples -> (word, freq)


def get_avg_complexity_all_users(users):
    """
    Calculates the average complexity of all users.

    :param users: List of models "User"
    :returns: float with 2 decimals after .
    """
    avg = 0

    for u in users:
        avg = avg + get_avg_complexity(Text.objects.filter(user_owner_id=u.pk))

    return round(avg / len(users), 2)


def get_texts_by_category(texts):
    """
    Filter how many texts are present in each category.
    :param texts: Set of models "Text".
    :return: how many texts are present in each category.
    """
    all_categories_frequency = []
    for t in texts:
        if t.category_id:
            analysis = [t.category]
            all_categories_frequency.append(analysis)
        else:
            all_categories_frequency.append([Category(pk=0, name='Nessuna categoria')])  # Creates a volatile category

    ordered_categories_frequency = sum((Counter(x) for x in all_categories_frequency), Counter())
    ordered_categories_frequency = ordered_categories_frequency.most_common()

    return ordered_categories_frequency  # list of tuples -> (category, number_texts)
