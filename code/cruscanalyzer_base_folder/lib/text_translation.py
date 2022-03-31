from googletrans import Translator, LANGUAGES


def translate(word, src, dest):
    """
    Function that translates a word into a chosen language

    Uses Google Translate API.

    :param word: word to translate
    :param src: source language prefix
    :param dest: target language prefix
    :type word: String
    :type src: String
    :type dest: String
    :raises: TypeError
    :returns: Translated word
    """
    trans = Translator()
    if type(word) != str:
        raise TypeError
    else:
        t = trans.translate(word, src=src, dest=dest)

    return t.text


def detect_language(word):
    """
    Identifies the source language of a word

    Uses Google Translate API to detect the language of the word.

    :param word: Word to detect the language of
    :type word: String
    :raises: TypeError
    :returns: Language prefix
    """
    det = Translator()
    if type(word) != str:
        raise TypeError
    else:
        dt = det.detect(word)

    return dt.lang


def get_languages():
    """
    Gets the dictionary of languages of Google Translate.

    {'prefix':'language'}
    es: 'it':'italiano'

    :returns: The dictionary of languages
    """
    return LANGUAGES
