import typing


class Block:
    _block_type: str

    def __init__(self, block_id: str = ""):
        if self._block_type is None:
            raise NotImplemented("All new block instances must have a _block_type")
        self._block = {"type": self._block_type, "block_id": block_id}

    def _set_block_attribute(self, attr, value):
        self._block.update({attr, value})
        return self

    def _update_block(self, d: dict):
        self._block.update(d)
        return self

    # TODO: implement accessories
    def set_block_accessory(self, accessory):
        ...


class SectionBlock(Block):
    _block_type = "section"

    def __init__(self, text: str, block_id: str = ""):
        super(SectionBlock, self).__init__(block_id=block_id)
        self._update_block({"text": {"type": "mrkdwn", "text": text}})

    @property
    def text(self):
        return self.text["text"]

    def set_text(self, text: str):
        if len(text) >= 3000:
            raise ValueError("Slack text cannot be greater than 3000 chars")
        self._set_block_attribute("text", text)
        return self


class ActionBlock(Block):
    _block_type = "actions"

    def __init__(self, block_id=""):
        super(ActionBlock, self).__init__(block_id=block_id)
        self._update_block({"elements": []})
        self._elements: list = self._block["elements"]

    # TODO: element implementation and assertion
    def set_element(self, element):
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
        # TODO: implement text elements here
        self._set_block_attribute("title", {"type": "mrkdwn", "text": title})


class ContextBlock(Block):
    # TODO: implement objects
    _block_type = "context"

    def __init__(self, block_id: str = "", elements: typing.List = []):
        super(ContextBlock, self).__init__(block_id=block_id)


class FileBlock(Block):
    """
    https://api.slack.com/reference/messaging/blocks#file
    """

    _block_type = "file"

    def __init__(self, block_id: str, source: str, external_id: str):
        super(FileBlock, self).__init__(block_id=block_id)
        self._update_block({"external_id": external_id, "source": source})
