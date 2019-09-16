import pytest

from simple_slack.utils import (
    value_length_constraint,
    list_to_csv,
    RenderedSlackElement,
)


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


def test_rendered_slack_elements():
    class Foo(RenderedSlackElement):
        def __init__(self):
            self._element = {"text": "some_text"}
            super(Foo, self).__init__(mappable=self._element)

        def _update_element(self, d):
            self._element.update(d)

    f = Foo()
    f._update_element({"param": 3, "other_foo": Foo(), "foo_list": [Foo(), Foo()]})
    assert f.render() == {
        "text": "some_text",
        "param": 3,
        "other_foo": {"text": "some_text"},
        "foo_list": [{"text": "some_text"}, {"text": "some_text"}],
    }
