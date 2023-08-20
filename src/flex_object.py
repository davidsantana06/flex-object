from typing import Any, Dict
from types import MethodType
from os.path import abspath, dirname, join
import json


class FlexObject(object):
    def __init__(self, **attrs) -> None:
        self.set_attrs(**attrs)

    def all_var_attrs(self) -> Dict[str, Any]:
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

    def to_json(self, file_path: str = '', indent: int = 4) -> None:
        if not file_path:
            file_path = join(
                abspath(dirname(__file__)),
                f'{self.__class__.__name__}.json'
            )

        with open(file_path, "w") as json_file:
            json.dump(self.all_var_attrs(), json_file, indent=indent)
