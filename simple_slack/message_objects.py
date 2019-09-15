import typing
import logging
import json
from urllib.parse import quote
from webbrowser import open
from pprint import pformat

from simple_slack.blocks import Block
from simple_slack.utils import RenderedSlackElement


logger = logging.getLogger(__name__)


class Message(RenderedSlackElement):
    """
    Inherits arguments from: https://api.slack.com/methods/chat.postMessage
    """

    def __init__(self):
        self.content: typing.Dict = {"blocks": [], "as_user": False, "mrkdwn": True}
        super(Message, self).__init__(self.content)

    def __repr__(self) -> str:
        return f"<SlackMessage {pformat(self.content)}>"

    def preview_blocks(self):
        """
        Open in Slack block kit builder preview
        :return:
        """
        if not self.blocks:
            logger.warning("Cannot block preview message without any blocks!")
        else:
            open(
                f'https://api.slack.com/tools/block-kit-builder?blocks={quote(json.dumps(self.render()["blocks"]))}'
            )

    def _set_content_attribute(self, attr, value):
        self.content[attr] = value

    def add_block(self, block: Block):
        self.content["blocks"].append(block)
        return self

    @property
    def blocks(self):
        return self.content["blocks"]

    @blocks.setter
    def blocks(self, blocks: typing.List[Block]):
        self.content["blocks"] = blocks

    @property
    def text(self) -> str:
        return self.content["text"]

    @text.setter
    def text(self, text):
        self.content["text"] = text

    @property
    def as_user(self) -> bool:
        return self.content["as_user"]

    @as_user.setter
    def as_user(self, as_user: bool):
        self._set_content_attribute("as_user", as_user)

    @property
    def username(self):
        return self.content.get("username")

    @username.setter
    def username(self, username: str):
        self._set_content_attribute("username", username)

    @property
    def mrkdwn(self):
        return self.content["mrkdwn"]

    @mrkdwn.setter
    def mrkdwn(self, value: bool):
        self._set_content_attribute("mrkdwn", value)

    @property
    def icon_emoji(self):
        return self.content.get("icon_emoji")

    @icon_emoji.setter
    def icon_emoji(self, value: str):
        self._set_content_attribute("icon_emoji", value)

    @property
    def icon_url(self):
        return self.content.get("icon_url")

    @icon_url.setter
    def icon_url(self, value: str):
        self._set_content_attribute("icon_url", value)
