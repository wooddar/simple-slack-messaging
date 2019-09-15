"""
https://api.slack.com/reference/messaging/composition-objects
"""
from pprint import pformat

from simple_slack.utils import RenderedSlackElement


class BlockObject(RenderedSlackElement):
    def __init__(self):
        self._object = {}
        super(BlockObject, self).__init__(self._object)

    def __repr__(self) -> str:
        return pformat(self._object)

    def _set_object_attribute(self, attr, value):
        self._object[attr] = value
        return self

    def _update_object(self, d):
        self._object.update(d)


class Text(BlockObject):
    """
    https://api.slack.com/reference/messaging/composition-objects#text
    """

    def __init__(
        self, text, text_type="mrkdwn", verbatim: bool = False, emoji: bool = False
    ):
        super(Text, self).__init__()
        self._update_object(
            {"type": text_type, "text": text, "verbatim": verbatim, "emoji": emoji}
        )


class ConfirmationDialog(BlockObject):
    """
    https://api.slack.com/reference/messaging/composition-objects#confirm
    """

    def __init__(self, title: str, text: str, confirm: str, deny: str):
        super(ConfirmationDialog, self).__init__()
        if len(title) >= 100:
            raise ValueError("Confirmation title must be < 100 chars")
        if len(text) >= 300:
            raise ValueError("Confirmation text must be < 300 chars")
        if any([len(confirm) >= 30, len(deny) >= 30]):
            raise ValueError(
                "Confirmation confirm and deny text must be each < 30 chars"
            )
        self._update_object(
            {
                "title": title,
                "text": {"type": "mrkdwn", "text": text},
                "confirm": {"type": "plain_text", "text": confirm},
                "deny": {"type": "plain_text", "text": deny},
            }
        )


class SelectOption(BlockObject):
    """
    https://api.slack.com/reference/messaging/composition-objects#option
    """

    def __init__(self, text: str, value: str, url: str = ""):
        super(SelectOption, self).__init__()
        if len(url) >= 3000:
            raise ValueError("Slack Select option text must be < 3000 chars")
        self._update_object(
            {"text": {"type": "plain_text", "text": text}, "value": value}
        )
