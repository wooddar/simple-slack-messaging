import typing
import os
import logging
import requests

from pprint import pformat
from slack.web.client import WebClient
from slack.web.client import SlackResponse

from simple_slack import exception
from simple_slack.message_objects import Message
from simple_slack.utils import list_to_csv

logger = logging.getLogger(__name__)


class SlackMessenger:
    client: typing.Optional[WebClient]
    default_webhook: typing.Optional[str]

    def __init__(
        self,
        token: typing.Optional[str] = None,
        default_webhook: typing.Optional[str] = None,
        recipient_hook: typing.Optional[typing.Callable[[typing.Any], str]] = None,
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

        if recipient_hook is None:
            # Passthrough callable
            self.recipient_hook = lambda x: x
        else:
            self.recipient_hook = recipient_hook

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
        thread_ts: str = None,
    ) -> typing.Union[requests.Response, SlackResponse]:

        if not hasattr(message, "_can_render") and type(message) != str:
            raise ValueError(
                f"Only Valid Message objects may be sent\nGot type {type(message)}"
            )

        if type(message) == str:
            m = Message()
            m.text = message
            message = m

        recipient = self.recipient_hook(recipient)

        if self.client is not None:
            r = self.client.chat_postMessage(
                channel=recipient,
                text=message.text,
                blocks=[i.render() for i in message.blocks],
                as_user=message.as_user,
                icon_emoji=message.icon_emoji,
                icon_url=message.icon_url,
                mrkdwn=message.mrkdwn,
                thread_ts=thread_ts,
                username=message.username,
            )
            if not r.data["ok"]:
                raise exception.SlackBotMessageNotSent(
                    f"Slack message not sent {pformat(r.data)}"
                )
        else:
            r = requests.post(webhook or self.default_webhook, json=message.render())

        return r

    def send_file(
        self,
        file: typing.Union[bytes, str],
        recipient: typing.Union[str, typing.List[str]],
        thread_ts: float = None,
        title: str = None,
    ):
        """
        https://api.slack.com/methods/files.upload
        """
        recipient = self.recipient_hook(recipient)
        if type(recipient) == list:
            recipient = list_to_csv(recipient)

        if type(file) == str:
            file = open(file, "r").read()

        if self.client is None:
            raise exception.SlackMessengerException(
                f"Only Slack Messenger clients with tokens enabled can send files!"
            )
        else:
            return self.client.files_upload(
                channel=recipient, title=title, thread_ts=thread_ts, content=file
            )

    # TODO: implement dialogs
    def send_dialog(self, dialog, trigger_id: str):
        if self.client is None:
            raise exception.SlackMessengerException(
                f"Only Slack Messenger clients with tokens enabled can send dialogs"
            )
        else:
            return self.client.dialog_open(
                dialog=dialog.render(), trigger_id=trigger_id
            )
