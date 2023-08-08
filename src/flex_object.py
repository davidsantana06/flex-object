from types import MethodType


class FlexObject():
    def __init__(self, **attrs) -> None:
        self.set_attrs(**attrs)

    def set_attrs(self, **attrs) -> None:
        for name, value in attrs.items():
            if name.startswith('_'):
                continue
            else:
                if callable(value):
                    value = MethodType(value, self)

                setattr(self, name, value)

    def del_attrs(self, *attr_names):
        for name in attr_names:
            if not type(name) == str:
                continue
            else:
                if hasattr(self, name):
                    delattr(self, name)

    def to_excel(self, file_name: str = None, folder_path: str = None) -> None:
        pass

    def to_json(self, file_name: str = None, folder_path: str = None) -> None:
        pass
