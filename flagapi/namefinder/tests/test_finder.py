import pytest

from flagapi.namefinder.views import find_names, find_names_position, replace_names


@pytest.mark.parametrize("sentence,names",
                         [
                             ("Mary got a little lamb.", ["Mary"]),
                             ("Carlos is doing a good job.", ["Carlos"]),
                             ("My name is Bond, James Bond.", ["James"]),
                             ("Silvio Santos is a famous anchor in Brazil.", ["Silvio", "Santos"]),
                         ]
                         )
def test_find_names(sentence, names):
    names_found = find_names(sentence)
    assert len(names_found) == len(names), "Number of names found is different than the number of names expected"
    for name in names:
        assert name in names_found, "Name expected was not found."


@pytest.mark.parametrize("sentence,positions",
                         [
                             ("Mary got a little lamb.", [(0, 4)]),
                             ("Carlos is doing a good job.", [(0, 6)]),
                             ("My name is Bond, James Bond.", [(17, 22)]),
                             ("Silvio Santos is a famous anchor in Brazil.", [(0, 6), (7, 13)]),
                         ]
                         )
def test_names_position(sentence, positions):
    positions_found = find_names_position(sentence)
    assert sorted(positions_found) == sorted(positions), "Name position is different that name position expected"


@pytest.mark.parametrize("sentence,replace",
                         [
                             ("Mary got a little lamb.", "XXXX got a little lamb."),
                             ("Silvio Santos is famous in Brazil.", "XXXXXX XXXXXX is famous in Brazil."),
                         ]
                         )
def test_replace_names(sentence, replace):
    assert replace_names(sentence) == replace, "Sentence with replaced name is different that the expected."


@pytest.mark.parametrize("sentence,replace",
                         [
                             ("Carlos is doing a good job.", "------ is doing a good job."),
                         ]
                         )
def test_replace_names_to_replace(sentence, replace):
    assert replace_names(sentence, to_replace="-") == replace, \
        "Sentence with replaced name is different that the expected."


@pytest.mark.parametrize("sentence,replace",
                         [
                             ("My name is Bond, James Bond.", "My name is Bond, XXXXXXXXXX Bond."),
                         ]
                         )
def test_replace_names_fixed_size(sentence, replace):
    assert replace_names(sentence, fixed_size=10) == replace, \
        "Sentence with replaced name is different that the expected."


@pytest.mark.parametrize("sentence,replace",
                         [
                             ("My name is Bond, James Bond.", "My name is Bond, .......... Bond."),
                         ]
                         )
def test_replace_names_to_replace_and_fixed_size(sentence, replace):
    assert replace_names(sentence, to_replace=".", fixed_size=10) == replace, \
        "Sentence with replaced name is different that the expected."
