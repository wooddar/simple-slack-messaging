# simple-slack-messaging
[![CircleCI](https://circleci.com/gh/wooddar/simple-slack-messaging/tree/master.svg?style=svg)](https://circleci.com/gh/wooddar/simple-slack-messaging/tree/master)

# Installation
`pip install simple-slack-messaging`

Put in env vars

## Usage
```python
from simple_slack import SlackMessenger, Message

greeting_message = Message()
greeting_message.text = "Hello I am a Slack message!"

```
