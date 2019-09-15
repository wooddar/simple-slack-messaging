import typing
from pprint import pformat
from simple_slack.blocks import block_accessories
from simple_slack.blocks import block_objects
from simple_slack.utils import RenderedSlackElement


class Block(RenderedSlackElement):
    _block_type: str

    def __init__(self, block_id: str = ""):
        if self._block_type is None:
            raise NotImplemented("All new block instances must have a _block_type")
        self._block: typing.Dict = {"type": self._block_type, "block_id": block_id}
        super(Block, self).__init__(self._block)

    def __repr__(self) -> str:
        return pformat(self._block)

    def _set_block_attribute(self, attr, value):
        self._block.update({attr, value})
        return self

    def _update_block(self, d: dict):
        self._block.update(d)
        return self

    def set_block_accessory(self, accessory: block_accessories.BlockAccessory):
        self._block["accessory"] = accessory


class SectionBlock(Block):
    _block_type = "section"

    def __init__(self, text: typing.Union[str, block_objects.Text], block_id: str = ""):
        super(SectionBlock, self).__init__(block_id=block_id)
        if type(text) == str:
            text = block_objects.Text(text=text)
        self._update_block({"text": text})


class ActionBlock(Block):
    _block_type = "actions"

    def __init__(self, block_id=""):
        super(ActionBlock, self).__init__(block_id=block_id)
        self._update_block({"elements": []})
        self._elements: list = self._block["elements"]

    def set_element(self, element: block_objects.BlockObject):
        self._elements.append(element)
        return self

    def get_elements(self):
        return self._elements


class DividerBlock(Block):
    _block_type = "divider"


class ImageBlock(Block):
    """
    https://api.slack.com/reference/messaging/blocks#image
    """

    _block_type = "image"

    def __init__(self, image_url: str, alt_text: str, title: str, block_id=""):
        super(ImageBlock, self).__init__(block_id=block_id)
        if len(alt_text) > 2000:
            raise ValueError("Slack image block alt text cannot be > 2000 chars")
        self._set_block_attribute("alt_text", alt_text)
        self._set_block_attribute("image_url", image_url)
        self._set_block_attribute("title", {"type": "plain_text", "text": title})


class ContextBlock(Block):
    _block_type = "context"

    def __init__(
        self, elements: typing.List[block_objects.BlockObject], block_id: str = ""
    ):
        super(ContextBlock, self).__init__(block_id=block_id)
        self._update_block({"elements": elements})


class FileBlock(Block):
    """
    https://api.slack.com/reference/messaging/blocks#file
    """

    _block_type = "file"

    def __init__(self, block_id: str, source: str, external_id: str):
        super(FileBlock, self).__init__(block_id=block_id)
        self._update_block({"external_id": external_id, "source": source})
