from django.conf import settings

from flagapi.namefinder.exceptions import VariableNotSet, ParameterMissing


def get_first_names_pack():
    return getattr(settings, 'FIRST_NAMES', None)


def get_last_names_pack():
    return getattr(settings, 'LAST_NAMES', [])


def get_no_names_pack():
    return getattr(settings, 'NO_NAMES', [])


def find_names(sentence=None):
    """
    Find names in a sentence based on a FIRST_NAMES file
    :param sentence: Sentence
    :return List of list of names
    """
    if not sentence:
        raise Exception(ParameterMissing, "This method requires sentence as input")

    if not isinstance(sentence, str):
        raise Exception(TypeError, "This method requires string as input")

    first_names = get_first_names_pack()
    if not first_names:
        raise Exception(VariableNotSet, "Variable FIRST_NAMES not set in settings.py")

    punctuation = '!@#$%^&*()_+<>?:.,;'

    for c in sentence:
        if c in punctuation:
            sentence = sentence.replace(c, " ")

    words = sentence.lower().split()
    res = set(words).intersection(first_names)

    to_return = [w.title() for w in res]

    return to_return


def find_names_position(sentence=None):
    """
    Find names position in a sentence based on a FIRST_NAMES file
    :param sentence: Sentence
    :return List of tuples (begin, end) position
    """
    if not sentence:
        raise Exception(ParameterMissing, "This method requires sentence as input")

    if not isinstance(sentence, str):
        raise Exception(TypeError, "This method requires string as input")

    names_found = find_names(sentence)

    to_return = []
    for name in names_found:
        begin = sentence.lower().index(name.lower())
        end = begin + len(name)
        to_return.append((begin, end))

    return to_return


def replace_names(sentence=None, to_replace="X", fixed_size=0):
    """
    Find names in a sentence based on a FIRST_NAMES file and replace them
    :param sentence: Sentence
    :param to_replace: Character to be used for replaced names
    :param fixed_size: If greater than 0 the name will be replaced by fixed_size * to_replace
    :return The same sentence with replaced names.
    """
    if not sentence:
        raise Exception(ParameterMissing, "This method requires sentence as input")

    if not isinstance(sentence, str):
        raise Exception(TypeError, "This method requires string as input")

    positions_found = find_names_position(sentence)

    for position in positions_found:
        begin, end = position
        word = sentence[begin: end]
        if fixed_size > 0:
            size = fixed_size
        else:
            size = end - begin
        replace = to_replace * size
        sentence = sentence.replace(word, replace)

    return sentence
