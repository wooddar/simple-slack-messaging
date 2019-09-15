"""
https://api.slack.com/reference/messaging/composition-objects
"""


class BlockAccessory:

    def __init__(self):
        self._accessory = {
            'type': self._accessory_type
        }

    def __getattr__(self, item):
        return self._accessory[item]

    def __setattr__(self, key, value):
        return self._set_accessory_attribute(key, value)

    def _set_accessory_attribute(self, attr, value):
        self._accessory[attr] = value
        return self

    def _update_accessory(self, d):
        self._accessory.update(d)

    def render(self):
        return self._accessory


class Text(BlockAccessory):
    ...


class Confirm(BlockAccessory):
    ...