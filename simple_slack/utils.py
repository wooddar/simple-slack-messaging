import typing
from functools import reduce


class RenderedSlackElement:
    def __init__(self, mappable: typing.Dict):
        self._mappable_obj = mappable

    def render(self):
        m_copy = {}
        for k, o in self._mappable_obj.items():
            if issubclass(type(o), self.__class__):
                m_copy[k] = o.render()
            else:
                m_copy[k] = o
        return m_copy


def list_to_csv(l: typing.List[str]):
    return ",".join(l)


def value_length_constraint(
    value, constraint: typing.Union[int, float], constraint_name: str
):
    if len(value) >= constraint and value is not None:
        raise ValueError(
            f"Slack constraint {constraint} not valid for value {constraint_name}: len {len(value)}"
        )
