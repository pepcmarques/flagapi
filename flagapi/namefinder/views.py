import re

from django.conf import settings

from flagapi.namefinder.exceptions import VariableNotSet, ParameterMissing


def get_first_names_pack():
    return getattr(settings, 'FIRST_NAMES', None)


def get_last_names_pack():
    return getattr(settings, 'LAST_NAMES', [])


def get_no_names_pack():
    return getattr(settings, 'NO_NAMES', [])


def find_names(sentence=None, last_names_enabled=True, no_names_enabled=False):
    """
    Find names in a sentence based on a FIRST_NAMES file
    :param sentence: Sentence
    :param last_names_enabled: boolean, if True add LAST_NAMES from FIRST_NAMES
    :param no_names_enabled: boolean, if True remove NO_NAMES from FIRST_NAMES
    :return List of list of names
    """
    if not sentence:
        raise Exception(ParameterMissing, "This method requires sentence as input")

    if not isinstance(sentence, str):
        raise Exception(TypeError, "This method requires string as input")

    first_names = get_first_names_pack()
    if not first_names:
        raise Exception(VariableNotSet, "Variable FIRST_NAMES is not set in settings.py")

    if last_names_enabled:
        last_names = get_last_names_pack()
        if not last_names:
            raise Exception(VariableNotSet, "Variable LAST_NAMES is not set in settings.py")
        first_names = list(set(first_names).union(set(last_names)))

    if no_names_enabled:
        no_names = get_no_names_pack()
        if not no_names:
            raise Exception(VariableNotSet, "Variable NO_NAMES is not set in settings.py")
        first_names = list(set(first_names).difference(set(no_names)))

    punctuation = '!@#$%^&*()_+<>?:.,;'

    for c in sentence:
        if c in punctuation:
            sentence = sentence.replace(c, " ")

    words = sentence.lower().split()
    res = set(words).intersection(first_names)

    to_return = [w.title() for w in res]

    return to_return


def find_names_position(sentence=None, last_names_enabled=True, no_names_enabled=False):
    """
    Find names position in a sentence based on a FIRST_NAMES file
    :param sentence: Sentence
    :param last_names_enabled: boolean, if True add LAST_NAMES from FIRST_NAMES
    :param no_names_enabled: boolean, if True remove NO_NAMES from FIRST_NAMES
    :return List of tuples (begin, end) position
    """
    if not sentence:
        raise Exception(ParameterMissing, "This method requires sentence as input")

    if not isinstance(sentence, str):
        raise Exception(TypeError, "This method requires string as input")

    names_found = find_names(sentence, last_names_enabled=last_names_enabled, no_names_enabled=no_names_enabled)

    to_return = []
    for name in names_found:
        begin_positions = [m.start() for m in re.finditer(name, sentence)]
        for begin in begin_positions:
            to_return.append((begin, begin + len(name)))
        # begin = sentence.lower().index(name.lower())
        # end = begin + len(name)
        # to_return.append((begin, end))

    return to_return


def replace_names(sentence=None, to_replace="X", fixed_size=0, last_names_enabled=True, no_names_enabled=False):
    """
    Find names in a sentence based on a FIRST_NAMES file and replace them
    :param sentence: Sentence
    :param to_replace: Character to be used for replaced names
    :param fixed_size: If greater than 0 the name will be replaced by fixed_size * to_replace
    :param last_names_enabled: boolean, if True add LAST_NAMES from FIRST_NAMES
    :param no_names_enabled: boolean, if True remove NO_NAMES from FIRST_NAMES
    :return The same sentence with replaced names.
    """
    if not sentence:
        raise Exception(ParameterMissing, "This method requires sentence as input")

    if not isinstance(sentence, str):
        raise Exception(TypeError, "This method requires string as input")

    positions_found = find_names_position(sentence, last_names_enabled=last_names_enabled,
                                          no_names_enabled=no_names_enabled)

    words_to_do = set()
    for position in positions_found:
        begin, end = position
        word = sentence[begin: end]
        words_to_do.add(word)

    for word in words_to_do:
        if fixed_size > 0:
            size = fixed_size
        else:
            size = end - begin
        replace = to_replace * size
        sentence = sentence.replace(word, replace)

    return sentence
