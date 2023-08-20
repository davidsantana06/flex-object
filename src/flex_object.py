from typing import Any, Dict, Tuple
from types import MethodType, NoneType
from os.path import abspath, dirname, join
import json


class FlexObject(object):
    def __init__(self, **attrs) -> None:
        self.set_attrs(**attrs)

    def set_attrs(self, **attrs) -> None:
        for name, value in attrs.items():
            if callable(value):
                value = MethodType(value, self)

            setattr(self, name, value)

    def del_attrs(self, *attr_names) -> None:
        for name in attr_names:
            if type(name) != str:
                continue
            else:
                if hasattr(self, name):
                    delattr(self, name)

    @staticmethod
    def json_safe_types() -> Tuple[type]:
        return (
            NoneType,               # none/null
            bool, float, int, str,  # primitive variables
            dict, list, tuple       # data structures
        )

    def json_safe_attrs(self) -> Dict[str, Any]:
        return {
            name: value
            for name, value in self.__dict__.items()
            if type(value) in self.json_safe_types()
        }

    def to_json(self, indent: int = 4) -> str:
        data: Dict[str, Any] = self.json_safe_attrs()
        json_str: str = json.dumps(data, indent=indent)
        return json_str

    def write_json(self, file_path: str = '', indent: int = 4) -> None:
        if not file_path:
            file_path = join(
                abspath(dirname(__file__)),
                f'{self.__class__.__name__}.json'
            )
        data: Dict[str, Any] = self.json_safe_attrs()

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=indent)
