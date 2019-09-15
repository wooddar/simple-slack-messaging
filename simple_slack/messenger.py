import typing
import os
import logging

from slack.web.client import WebClient

from simple_slack import exception
from simple_slack.message_objects import Message

logger = logging.getLogger(__name__)


class SlackMessenger:
    def __init__(
        self,
        token: typing.Optional[str] = None,
        default_webhook: typing.Optional[str] = None,
        **kwargs,
    ):
        mt = token or os.getenv("SLACK_TOKEN")
        if mt is not None:
            self.client = WebClient(token=mt, **kwargs)
        else:
            self.client = None
            logger.warning(
                f"Cannot start Slack Messenger in bot mode, falling back to default webhooks"
            )

        dw = default_webhook or os.getenv("SLACK_DEFAULT_WEBHOOK_URL")

        if dw is not None:
            self.default_webhook = dw
        else:
            logger.warning("Cannot start Slack Messenger in default webhook mode")
            self.default_webhook = None

        if dw is None and mt is None:
            raise RuntimeError(
                f"Cannot start a Slack Messenger Client without either a default webhook URL or token"
            )

    def send_message(
        self,
        message: typing.Union[Message, str],
        recipient: typing.Optional[str] = None,
        webhook: typing.Optional[str] = None,
    ):
        if self.client is not None:
            self.client.chat_postMessage(
                channel=recipient,
                text=message.text,
                blocks=message.blocks,
                attachments=message.attachments,
            )
        ...

    def send_file(self, recipient):
        if self.client is None:
            raise exception.SlackMessengerException(
                f"Only Slack Messenger clients with tokens enabled can send files!"
            )

    def send_dialog(self, message_ts):
        if self.client is None:
            raise exception.SlackMessengerException(
                f"Only Slack Messenger clients with tokens enabled can send dialogs"
            )
