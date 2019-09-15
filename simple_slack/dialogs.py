import typing

from pprint import pformat

from simple_slack.utils import RenderedSlackElement, value_length_constraint


class BaseSlackDialogElement(RenderedSlackElement):
    _element_type: str

    def __init__(self, name: str, label: str, optional: bool = True):
        value_length_constraint(name, 300, "name")
        value_length_constraint(name, 48, "label")
        if self._element_type is None:
            raise NotImplemented(
                "Cannot implement Slack dialog element with no _element_type specified"
            )
        self._dialog_element: typing.Dict = {
            "label": label,
            "name": name,
            "optional": optional,
            "type": self._element_type,
        }
        super(BaseSlackDialogElement, self).__init__(self._dialog_element)

    def __repr__(self) -> str:
        return pformat(self._dialog_element)

    def _update_element(self, d):
        self._dialog_element.update(d)

    def _set_element_attribute(self, attr, value):
        self._dialog_element[attr] = value


class Text(BaseSlackDialogElement):
    _element_type = "text"

    def __init__(
        self,
        max_length: int = None,
        min_length: int = None,
        hint: str = None,
        subtype: str = None,
        value: str = None,
        placeholder: str = None,
        **kwargs,
    ):
        super(Text, self).__init__(**kwargs)
        value_length_constraint(max_length, 150, "max_length")
        value_length_constraint(min_length, 150, "min_length")
        value_length_constraint(value, 150, "value")
        value_length_constraint(placeholder, 150, "placeholder")
        value_length_constraint(hint, 150, "hint")
        self._update_element(
            {
                "max_length": max_length,
                "min_length": min_length,
                "subtype": subtype,
                "value": value,
                "placeholder": placeholder,
                "hint": hint,
            }
        )


class TextArea(BaseSlackDialogElement):
    _element_type = "textarea"

    def __init__(
        self,
        max_length: int = None,
        min_length: int = None,
        hint: str = None,
        subtype: str = None,
        value: str = None,
        placeholder: str = None,
        **kwargs,
    ):
        super(TextArea, self).__init__(**kwargs)
        value_length_constraint(max_length, 3000, "max_length")
        value_length_constraint(min_length, 3000, "min_length")
        value_length_constraint(value, 3000, "value")
        value_length_constraint(placeholder, 150, "placeholder")
        value_length_constraint(hint, 150, "hint")
        self._update_element(
            {
                "max_length": max_length,
                "min_length": min_length,
                "subtype": subtype,
                "value": value,
                "placeholder": placeholder,
                "hint": hint,
            }
        )


class Select(BaseSlackDialogElement):
    _element_type = "select"

    def __init__(
        self,
        min_query_length: int = None,
        subtype: str = None,
        value: str = None,
        placeholder: str = None,
        data_source: str = "static",
        **kwargs,
    ):
        super(Select, self).__init__(**kwargs)
        value_length_constraint(min_query_length, 100, "min_length")
        value_length_constraint(placeholder, 150, "placeholder")
        self._update_element(
            {
                "data_source": data_source,
                "min_query_length": min_query_length,
                "subtype": subtype,
                "options": [],
                "value": value,
                "placeholder": placeholder,
            }
        )

    def add_option(self, label: str, value: str):
        self._dialog_element["options"].append({"label": label, "value": value})


class SlackDialog(RenderedSlackElement):
    def __init__(
        self,
        title,
        callback_id,
        state: str = None,
        submit_label=None,
        notify_on_cancel: bool = False,
    ):
        self._dialog = {
            "title": title,
            "state": state,
            "callback_id": callback_id,
            "elements": [],
            "submit_label": submit_label,
            "notify_on_cancel": notify_on_cancel,
        }
        super(SlackDialog, self).__init__(self._dialog)

    def __repr__(self) -> str:
        return pformat(self._dialog)

    def add_element(self, element: BaseSlackDialogElement):
        self._dialog["elements"].append(element)

    def render(self):
        if not self._dialog["elements"]:
            raise ValueError(
                f"Cannot render dialog {self._dialog['callback_id']} with no elements"
            )
        return super(SlackDialog, self).render()
