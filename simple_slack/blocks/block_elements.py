"""
This module provides implementations for Slack block elements - at present only basic actions and
selects are implemented.

https://api.slack.com/reference/messaging/block-elements
"""
import typing
import logging

logger = logging.getLogger(__name__)


class BlockElement:
    _element_type: str

    def __init__(self):
        if self._element_type is None:
            raise NotImplemented("Block elements must implement _element_type param")
        self._element: typing.Dict = {"type": self._element_type}

    def __getattr__(self, item):
        return self._get_element_attribute(item)

    def __setattr__(self, key, value):
        return self._set_element_attribute(key, value)

    def _update_element(self, d):
        self._element.update(d)
        return self

    def _set_element_attribute(self, attr, value):
        self._element[attr] = value

    def _get_element_attribute(self, attr):
        return self._element[attr]

    def render(self):
        return self._element


class ImageElement(BlockElement):
    """
    https://api.slack.com/reference/messaging/block-elements#image
    """

    _element_type = "image"

    def __init__(self, image_url: str, alt_text: str):
        super(ImageElement, self).__init__()
        self._update_element({"image_url": image_url, "alt_text": alt_text})


class ButtonElement(BlockElement):
    """
    https://api.slack.com/reference/messaging/block-elements#button
    """

    _element_type = "button"

    # TODO: implement Text Objects
    def __init__(self, text: str, action_id: str):
        super(ButtonElement, self).__init__()
        self._update_element(
            {"text": {"type": "mrkdwn", "text": text}, "action_id": action_id}
        )

    def set_url(self, url: str):
        if len(url) > 3000:
            raise ValueError(
                "Slack Action button URLs cannot be longer than 3000 chars"
            )
        return self._set_element_attribute("url", url)

    def set_value(self, value: str):
        if len(value) > 2000:
            raise ValueError("Slack Action button Values cannot be > 2000 chars")
        return self._set_element_attribute("value", value)

    def set_style(self, style: str):
        if style not in ["primary", "danger", "default"]:
            raise ValueError(f"Unrecognised Slack action button style value {style}")
        return self._set_element_attribute("style", style)

    # TODO: implement confirm objects here
    def set_confirm(self, confirm):
        return self._set_element_attribute("confirm", confirm)


class SelectMenuElement(BlockElement):
    """
    https://api.slack.com/reference/messaging/block-elements#select
    """

    _element_type = "static_select"
    # TODO: implement text objects

    def __init__(self, placeholder: str, action_id: str):
        super(SelectMenuElement, self).__init__()
        self._update_element(
            {
                "placeholder": {"type": "mrkdwn", "text": placeholder},
                "action_id": action_id,
                "options": [],
            }
        )
        self._options: list = self._element["options"]

    # TODO: implement option object
    def add_option(self, option):
        self._options.append(option)
        return self

    def get_options(self):
        return self._options

    def render(self):
        if not self._options:
            raise ValueError("Select menu must have one or more options")
        return super(SelectMenuElement, self).render()
