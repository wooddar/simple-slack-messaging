class SlackMessengerException(Exception):
    ...


class SlackBotMessageNotSent(SlackMessengerException):
    ...


class SlackWebhookMessageNotSent(SlackMessengerException):
    ...
