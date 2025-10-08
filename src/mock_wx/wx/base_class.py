from argparse import Namespace
from unittest.mock import Mock

G_APP = None
G_MOCK = Mock()
G_OBJS = Namespace()


class BaseClass:
    def __init__(self, *args, **kwargs):
        if "name" in kwargs:
            name = kwargs["name"]
            if name in ["dut", "app"]:
                self._name = f"self.{name}"
                self._mock = getattr(G_MOCK, name)
            else:
                self._name = f"self.dut.{name}"
                self._mock = getattr(G_MOCK.dut, name)
        else:
            name = self.__class__.__name__
            self._mock = getattr(G_MOCK, name)
            if name not in G_OBJS:
                setattr(G_OBJS, name, [])
            value = getattr(G_OBJS, name)
            self._name = f"self.objs.{name}[{len(value)}]"
            value.append(self)
        self._mock(*args, **kwargs)

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    def __getattr__(self, name):
        return getattr(self._mock, name)
