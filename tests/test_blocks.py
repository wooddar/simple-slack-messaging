import pytest
from simple_slack.blocks import Block, SectionBlock, ImageBlock, DividerBlock, ContextBlock, FileBlock
from simple_slack.blocks.block_accessories import ImageAccessory, ButtonAccessory
from simple_slack.blocks.block_objects import Text


def test_block_instances():
    sb = SectionBlock('hello', 'block')
    ib = ImageBlock(image_url='www.image.com.au', title='image title', alt_text='texty_image', block_id='image')
    db = DividerBlock('divider')
    cb = ContextBlock([Text('hello'), ImageAccessory(image_url='www.cat.jpg', alt_text='pic description')], 'context')


def test_inherited_block():
    with pytest.raises(NotImplemented):
        Block()


def test_block_render():
    sb = SectionBlock('hello')
    assert sb.render() == {
        'type':'section',
        'block_id':'',
        'text':{'text':'hello', 'type':'mrkdwn', 'verbatim':False}
    }

def test_add_accessory():
    sb = SectionBlock('hello')
    ia = ImageAccessory(image_url='https://catpics.jpg', alt_text='Some other damn photo')
    sb.set_block_accessory(ia)
    assert sb._block['accessory'] == ia
