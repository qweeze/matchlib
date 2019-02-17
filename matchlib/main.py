import re
from typing import Union


def matches(obj: Union[dict, list], partial: Union[dict, list]) -> bool:
    """Matches a given object against another
    which can contain "wildcard" elements (`...`)
    :return: bool
    """
    if isinstance(partial, dict) and isinstance(obj, dict):
        if ... in partial:
            keys = set(partial) - {...}
        else:
            keys = set(partial) | set(obj)
        for k in keys:
            if k not in partial or k not in obj:
                return False
            if partial[k] is ...:
                continue
            if not matches(obj[k], partial[k]):
                return False

        return True

    elif isinstance(partial, list) and isinstance(obj, list):
        obj_idx = 0
        skip = False
        for idx, el in enumerate(partial):
            if el is ...:
                if idx == len(partial) - 1:
                    return True
                skip = True
                continue
            if skip:
                while not matches(obj[obj_idx], el):
                    if obj_idx == len(obj) - 1:
                        return False
                    obj_idx += 1
                skip = False

            if obj_idx >= len(obj) or not matches(obj[obj_idx], el):
                return False

            obj_idx += 1

        if not skip and obj_idx != len(obj):
            return False

        return True

    return partial == obj


class Partial:
    def __init__(self, obj: Union[dict, list]):
        self.obj = obj

    def __eq__(self, other):
        return matches(other, self.obj)

    def __ne__(self, other):
        return not matches(other, self.obj)


class Regex:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags=flags)

    def __eq__(self, other):
        return isinstance(other, str) and self._regex.match(other) is not None

    def __ne__(self, other):
        return not self.__eq__(other)


Any = ...
