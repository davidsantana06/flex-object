from os.path import abspath, dirname, join
from pandas import DataFrame, Series
from typing import Any, Dict
from types import MethodType
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

    def __define_file_path(self, file_path: str, file_ext: str) -> str:
        if (not file_path) or (not file_path.endswith(file_ext)):
            file_path = join(
                abspath(dirname(__file__)),
                f'{self.__class__.__name__}.{file_ext}'
            )

        return file_path

    def to_excel(self, file_path: str = '') -> None:
        file_path = self.__define_file_path(file_path, 'xlsx')
        data: Dict[str, Any] = self.all_var_attrs()
        data_series: Series = Series(data)
        data_frame: DataFrame = data_series.to_frame().transpose()
        data_frame.to_excel(file_path, index=False)

    def to_json(self, file_path: str = '', indent: int = 4) -> None:
        file_path = self.__define_file_path(file_path, 'json')
        data: Dict[str, Any] = self.all_var_attrs()

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=indent)
