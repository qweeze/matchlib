import re


def matches(obj, pattern):
    if isinstance(pattern, dict) and isinstance(obj, dict):
        if ... in pattern:
            keys = set(pattern) - {...}
        else:
            keys = set(pattern) | set(obj)
        for k in keys:
            if k not in pattern or k not in obj:
                return False
            if pattern[k] is ...:
                continue
            if not matches(obj[k], pattern[k]):
                return False

        return True

    elif isinstance(pattern, list) and isinstance(obj, list):
        obj_idx = 0
        skip = False
        for idx, el in enumerate(pattern):
            if el is ...:
                if idx == len(pattern) - 1:
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

    return pattern == obj


class Partial:
    def __init__(self, obj):
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
