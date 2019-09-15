import typing
from pprint import pformat

from simple_slack.blocks import Block
from simple_slack.utils import RenderedSlackElement


class Message(RenderedSlackElement):
    def __init__(self):
        self.content = dict()
        super(Message, self).__init__(self.content)

    def __repr__(self) -> str:
        return pformat(self.content)

    def preview(self):
        """
        Open in Slack block kit builder preview
        :return:
        """

    def _set_content_attribute(self, attr, value):
        self.content[attr] = value

    @property
    def blocks(self):
        return self.content["blocks"]

    @blocks.setter
    def blocks(self, blocks: typing.List[Block]):
        self.content["blocks"] = blocks

    @property
    def text(self):
        return self.content["text"]

    @text.setter
    def text(self, text):
        self.content["text"] = text
