from typing import Any, Dict
from types import MethodType


class FlexObject():
    def __init__(self, **attrs) -> None:
        self.set_attrs(**attrs)

    def all_vars_attrs(self) -> Dict[str, Any]:
        return {
            name: value
            for name, value in self.__dict__.items()
            if not callable(value)
        }

    def set_attrs(self, **attrs) -> None:
        for name, value in attrs.items():
            if name.startswith('_'):
                continue
            else:
                if callable(value):
                    value = MethodType(value, self)

                setattr(self, name, value)

    def del_attrs(self, *attr_names) -> None:
        for name in attr_names:
            if not type(name) == str:
                continue
            else:
                if hasattr(self, name):
                    delattr(self, name)

    def to_excel(self, file_path: str = '') -> None:
        pass

    def to_json(self, file_path: str = '') -> None:
        pass
