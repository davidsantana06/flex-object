from typing import Any, Dict, Tuple
from types import NoneType
from os.path import abspath, dirname, join
import json


class FlexObject(object):
    def __init__(self, **attrs) -> None:
        self.set_attrs(**attrs)

    def set_attrs(self, **attrs) -> None:
        for name, value in attrs.items():
            if (not name.startswith('_')) and (not callable(value)):
                setattr(self, name, value)

    def del_attrs(self, *attr_names) -> None:
        for name in attr_names:
            if (type(name) == str) and (hasattr(self, name)):
                delattr(self, name)

    @staticmethod
    def safe_json_types() -> Tuple[type]:
        return (
            NoneType,               # none/null
            bool, float, int, str,  # primitive variables
            dict, list, tuple       # data structures
        )

    def safe_json_attrs(self) -> Dict[str, Any]:
        return {
            name: value
            for name, value in self.__dict__.items()
            if (
                (not name.startswith('_')) and
                (type(value) in self.safe_json_types())
            )
        }

    def from_json(self, json_str: str) -> None:
        attrs: Dict[str, Any] = json.load(json_str)
        self.set_attrs(**attrs)

    def to_json(self, indent: int = 4) -> str:
        data: Dict[str, Any] = self.safe_json_attrs()
        json_str: str = json.dumps(data, indent=indent)
        return json_str

    def read_json_file(self, file_path: str) -> None:
        with open(file_path, 'r') as json_file:
            attrs: Dict[str, Any] = json.load(json_file)
            self.set_attrs(**attrs)

    def write_json_file(self, file_path: str = '', indent: int = 4) -> None:
        if (not file_path) or (not file_path.endswith('.json')):
            file_path = join(
                abspath(dirname(__file__)),
                f'{self.__class__.__name__}.json'
            )
        attrs: Dict[str, Any] = self.safe_json_attrs()

        with open(file_path, 'w') as json_file:
            json.dump(attrs, json_file, indent=indent)
