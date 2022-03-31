from collections import Counter
from nltk import RegexpTokenizer


def analyze_text(source_text):
    """
    Returns the words of a text with their frequency.

    Uses NLTK RegexpTokenizer in order to tokenize lowered words not with only blank space but also with all the punctuation.

    :param source_text: Text to analyze
    :type source_text: String
    :raises: TypeError
    :returns: Counter object (sub-class of dict) with all the words and their frequency
    """
    if type(source_text) != str:
        raise TypeError
    else:
        regex_tokenizer = RegexpTokenizer(r"\w+")
        words_text = regex_tokenizer.tokenize(source_text.lower())
        return Counter(words_text)


def ari_complexity_text(source_text):
    """
    Calculate the complexity of a text.

    Uses RegexpTokenizer in order to tokenize words not with only blank space but also with all the punctuation.
    Complexity calculated with the ARI algorithm.

    :param source_text: Texto to calculate the complexity of.
    :type source_text: String
    :raises TypeError
    :returns: Float with two digit after decimal, representing the complexity.
    """
    if type(source_text) != str:
        raise TypeError
    else:
        regex_tokenizer = RegexpTokenizer(r'\w+')
        score = 0.0
        if len(source_text) > 0:
            words_text = regex_tokenizer.tokenize(source_text)
            sentences_text = source_text.split('.')
            # characters = re.sub("[\. \W]+", "", source_text) # Keeping only the characters that are not punctuation.
            score = 4.71 * (len(source_text) / len(words_text)) \
                    + 0.5 * (len(words_text) / len(sentences_text)) - 21.43
            return round(score, 2) if score > 0 else 0

