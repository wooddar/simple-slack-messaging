import pytest

from simple_slack.utils import value_length_constraint, list_to_csv


def test_value_constrainer():
    s = "hello I am a long stringy string please string me"
    with pytest.raises(ValueError):
        value_length_constraint(s, 10, "Stringy String")

    try:
        value_length_constraint(s, 1000, "Stringy String")
    except:
        pytest.fail("Error should not have been raised here")


def test_list_csv():
    assert (
        list_to_csv(["person", "house", "plant"]) == "person,house,plant"
    ), "CSV not correctly produced from string list"
