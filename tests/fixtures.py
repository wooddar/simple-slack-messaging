import pytest
from simple_slack.blocks import SectionBlock, DividerBlock
from simple_slack.blocks.block_objects import Text
from simple_slack.blocks.block_accessories import ImageAccessory
from simple_slack.message_objects import Message


@pytest.fixture
def test_basic_message():
    m = Message()
    m.text = "I am a messagey message"
    return m


@pytest.fixture
def test_complex_message():
    section = SectionBlock(text="Section text", block_id="idddd")
    section.add_field(Text("Some cool message field"))
    section.set_block_accessory(
        ImageAccessory(
            "https://images.google.com/cat.png", alt_text="Disappointing cat pic"
        )
    )
    m = Message()
    m.text = "Incoming!!!"
    m.blocks = [section, DividerBlock()]
    return m
