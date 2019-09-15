import typing


class BaseSlackComponent:
    def render(self) -> dict:
        ...


class Message(BaseSlackComponent):
    def __init__(self):
        self.content = dict()

    def preview(self):
        """
        Open in Slack block kit builder preview
        :return:
        """

    def _set_content_attribute(self):
        return self

    @property
    def blocks(self):
        return self.content["blocks"]

    @property
    def text(self):
        return self.content["text"]
