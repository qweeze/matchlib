import re
import typing as t


Matchable = t.Union[t.Dict[t.Any, t.Any], t.List[t.Any], t.Set[t.Any], t.Tuple[t.Any]]


def matches(obj: Matchable, partial: Matchable) -> bool:
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

        if ... in partial and partial[...] is not ...:
            remaining = set(obj) - set(partial) - {...}
            if len(remaining) != 1:
                return False

            return matches(obj[remaining.pop()], partial[...])

        return True

    elif isinstance(partial, set) and isinstance(obj, set):
        if ... in partial:
            return (partial - {...}).issubset(obj)
        else:
            return partial == obj

    elif (isinstance(partial, list) and isinstance(obj, list)) or (
        isinstance(partial, tuple) and isinstance(obj, tuple)
    ):
        obj_idx = 0
        for idx, el in enumerate(partial):
            if el is ...:
                if idx == len(partial) - 1:
                    return True

                for i2 in range(obj_idx, len(obj)):
                    if matches(obj[i2:], partial[idx + 1 :]):
                        return True

                return False

            if obj_idx >= len(obj) or not matches(obj[obj_idx], el):
                return False

            obj_idx += 1

        if obj_idx != len(obj):
            return False

        return True

    return partial == obj


class Partial:
    def __init__(self, obj: t.Union[t.Dict[t.Any, t.Any], t.List[t.Any]]) -> None:
        self.obj = obj

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (dict, list, set, tuple)):
            return matches(other, self.obj)
        return super().__eq__(other)

    def __ne__(self, other: object) -> bool:
        if isinstance(other, (dict, list, set, tuple)):
            return not matches(other, self.obj)
        return super().__ne__(other)


class Regex:
    def __init__(self, pattern: str, flags: int = 0) -> None:
        self._regex = re.compile(pattern, flags=flags)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, str) and self._regex.match(other) is not None

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


Any = ...
