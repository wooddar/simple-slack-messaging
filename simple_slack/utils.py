import typing
from functools import reduce


class RenderedSlackElement:
    _can_render = True

    def __init__(self, mappable: typing.Dict):
        self._mappable_obj = mappable

    def render(self):
        m_copy = {}
        for k, o in self._mappable_obj.items():
            if hasattr(o, "_can_render"):
                m_copy[k] = o.render()
            # Sub element is an iterable and may contain things that should be rendered
            elif type(o) == list:
                m_copy[k] = [i.render() if hasattr(i, "_can_render") else i for i in o]
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
