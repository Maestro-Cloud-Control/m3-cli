import sys


class _NoNoneSysPath(list):
    """
    Drop-in replacement for sys.path that silently rejects None entries.

    An editable install (.pth file) injects None into sys.path at some point
    during the test session. coverage >= 7.4 iterates sys.path on every traced
    function call and crashes with:
        TypeError: path should be string, bytes, os.PathLike or integer, not NoneType

    Replacing sys.path with this list ensures None can never enter it,
    regardless of when or how it is attempted.
    """

    def append(self, obj):
        if obj is not None:
            super().append(obj)

    def insert(self, index, obj):
        if obj is not None:
            super().insert(index, obj)

    def extend(self, iterable):
        super().extend(x for x in iterable if x is not None)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            super().__setitem__(key, [v for v in value if v is not None])
        elif value is not None:
            super().__setitem__(key, value)

    def __iadd__(self, other):
        self.extend(other)
        return self


# Replace at module import time — before pytest plugins, before coverage starts
sys.path = _NoNoneSysPath(x for x in sys.path if x is not None)
