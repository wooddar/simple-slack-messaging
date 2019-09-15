"""
This module provides implementations for Slack block elements - at present only basic actions and
selects are implemented.

https://api.slack.com/reference/messaging/block-elements
"""
import typing
import logging
from pprint import pformat
from simple_slack.utils import RenderedSlackElement
from simple_slack.blocks import block_objects

logger = logging.getLogger(__name__)


class BlockAccessory(RenderedSlackElement):
    _accessory_type: str

    def __init__(self):
        if self._accessory_type is None:
            raise NotImplemented("Block elements must implement _accessory_type param")
        self._accessory: typing.Dict = {"type": self._accessory_type}
        super(BlockAccessory, self).__init__(self._accessory)

    def __repr__(self) -> str:
        return pformat(self._accessory)

    def _update_accessory(self, d):
        self._accessory.update(d)
        return self

    def _set_accessory_attribute(self, attr, value):
        self._accessory[attr] = value

    def _get_accessory_attribute(self, attr):
        return self._accessory[attr]


class ImageAccessory(BlockAccessory):
    """
    https://api.slack.com/reference/messaging/block-elements#image
    """

    _accessory_type = "image"

    def __init__(self, image_url: str, alt_text: str):
        super(ImageAccessory, self).__init__()
        self._update_accessory({"image_url": image_url, "alt_text": alt_text})


class ButtonAccessory(BlockAccessory):
    """
    https://api.slack.com/reference/messaging/block-elements#button
    """

    _accessory_type = "button"

    def __init__(self, text: str, action_id: str):
        super(ButtonAccessory, self).__init__()
        self._update_accessory(
            {"text": {"type": "plain_text", "text": text}, "action_id": action_id}
        )

    def set_url(self, url: str):
        if len(url) > 3000:
            raise ValueError(
                "Slack Action button URLs cannot be longer than 3000 chars"
            )
        return self._set_accessory_attribute("url", url)

    def set_value(self, value: str):
        if len(value) > 2000:
            raise ValueError("Slack Action button Values cannot be > 2000 chars")
        return self._set_accessory_attribute("value", value)

    def set_style(self, style: str):
        if style not in ["primary", "danger", "default"]:
            raise ValueError(f"Unrecognised Slack action button style value {style}")
        return self._set_accessory_attribute("style", style)

    def set_confirm(self, confirm: block_objects.ConfirmationDialog):
        return self._set_accessory_attribute("confirm", confirm)


class SelectMenuAccessory(BlockAccessory):
    """
    https://api.slack.com/reference/messaging/block-elements#select
    """

    _accessory_type = "static_select"

    def __init__(self, placeholder: str, action_id: str):
        super(SelectMenuAccessory, self).__init__()
        self._update_accessory(
            {
                "placeholder": {"type": "plain_text", "text": placeholder},
                "action_id": action_id,
                "options": [],
            }
        )
        self._options: list = self._accessory["options"]

    def add_option(self, option: block_objects.SelectOption):
        self._options.append(option)
        return self

    def get_options(self):
        return self._options

    def render(self):
        if not self._options:
            raise ValueError("Select menu must have one or more options")
        return super(SelectMenuAccessory, self).render()
