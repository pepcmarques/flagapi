from django import urls

import pytest
import json


@pytest.mark.parametrize("task, sentence, expected", [
    ("flag_it", "Mary got a little lamb", "XXXX got a little lamb"),
    ]
)
def test_replace_name(client, task, sentence, expected):
    data = {"task": task,
            "sentences": [sentence]
            }
    url = urls.reverse('rest:simple_classification')
    response = client.post(url, json.dumps(data), content_type="application/json")
    response_data = response.data
    flag = response_data["sentences"][0][0]
    assert flag == expected


@pytest.mark.parametrize("expected", ["no data received"])
def test_no_data_received(client, expected):
    url = urls.reverse('rest:simple_classification')
    response = client.post(url, "", content_type="application/json")
    response_data = response.data
    error = response_data["error"]
    assert error == expected


@pytest.mark.parametrize("task, expected", [
    ("flag_it", "data format error"),
    ]
)
def test_wrong_json_structure(client, task, expected):
    data = {"task": task}
    url = urls.reverse('rest:simple_classification')
    response = client.post(url, json.dumps(data), content_type="application/json")
    response_data = response.data
    error = response_data["error"]
    assert error == expected


@pytest.mark.parametrize("task, sentence, expected", [
    ("flag_it", "My friend was abused", True),
    ("flag_it", "My friend plays basketball", False),
    ("wrong_task", "It doesn't matter", "task not recognized"),
    ]
)
def test_sentence(client, task, sentence, expected):
    data = {"task": task,
            "sentences": [sentence]
            }
    url = urls.reverse('rest:simple_classification')
    response = client.post(url, json.dumps(data), content_type="application/json")
    response_data = response.data
    try:
        flag = response_data["sentences"][0][1]
    except KeyError:
        flag = response_data["error"]
    assert flag == expected
