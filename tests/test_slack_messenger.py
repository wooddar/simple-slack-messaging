import pytest
from unittest.mock import patch, MagicMock

from .fixtures import test_basic_message, test_complex_message
from simple_slack.messenger import SlackMessenger
from simple_slack import exception


slack_client_path = "slack.web.client.WebClient.chat_postMessage"
requests_post_path = "requests.post"


def test_messenger_init():
    # Test fail with no env vars or params set
    with pytest.raises(RuntimeError):
        sm = SlackMessenger()
    try:
        sm = SlackMessenger(token="xoxb-EXAMPLE-QWtUxI4L4eRuQ4nT1Ivvj35D")
        sm = SlackMessenger(default_webhook="https://webmchookface.com/TG6NES")
    except:
        pytest.fail(
            "Both of these SlackMessenger instances should have successfully initiated"
        )


@patch(slack_client_path)
@patch(requests_post_path)
def test_messenger_bot_sending(rpp: MagicMock, sc: MagicMock, test_complex_message):

    sm = SlackMessenger(token="xoxb-EXAMPLE-QWtUxI4L4eRuQ4nT1Ivvj35D")
    sm.send_message(test_complex_message, recipient="C98GMX")
    sc.assert_called()
    rpp.assert_not_called()


@patch(slack_client_path)
@patch(requests_post_path)
def test_messenger_webhook_sending(rpp: MagicMock, sc: MagicMock, test_complex_message):
    sm = SlackMessenger(default_webhook="https://webmchookface.com/TG6NES")
    sm.send_message(test_complex_message)
    sc.assert_not_called()
    rpp.assert_called()


@patch(slack_client_path)
@patch(requests_post_path)
def test_recipient_hook(rpp: MagicMock, sc: MagicMock, test_complex_message):
    r_hook = MagicMock(return_value="The Fonz")

    sm = SlackMessenger(
        token="xoxb-EXAMPLE-QWtUxI4L4eRuQ4nT1Ivvj35D", recipient_hook=r_hook
    )
    sm.send_message(test_complex_message, recipient="C98GMX")
    r_hook.assert_called()
