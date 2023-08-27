from typing import Any, Dict, Tuple
from types import NoneType
from os.path import abspath, dirname, join
import json


class FlexObject(object):
    def __init__(self, **attrs) -> None:
        '''
        Initialize the object with specified attributes.

        This method is the constructor for the class. It initializes the object by
        calling the `set_attrs` method with the provided keyword arguments, which
        sets the attributes based on the provided values.

        Parameters:
        ----------
        **attrs : keyword arguments
            Attributes and their corresponding values to be set during object creation.

        Returns:
        -------
        None.

        Examples:
        --------
        >>> flex_obj = FlexObject(name='David Santana', age=21)
        >>> flex_obj.name
        'David Santana'
        >>> flex_obj.age
        21
        '''
        self.set_attrs(**attrs)

    def set_attrs(self, **attrs) -> None:
        '''
        Set attributes for the object.

        This method is responsible for assigning a set of attributes to the object.
        The format of the attributes is provided by **kargs, which means that each
        attribute must be defined individually.

        Parameters:
        ----------
        **attrs : keyword arguments
            Attributes to be incorporated into the object.

        Returns:
        -------
        None.

        Examples:
        --------
        >>> flex_obj: FlexObject = FlexObject()
        >>> flex_obj.set_attrs(developer='David Santana', github='davidsantana06')
        >>> flex_obj.developer
        'David Santana'
        >>> flex_obj.github
        'davidsantana06'
        '''
        for name, value in attrs.items():
            if (not name.startswith('_')) and (not callable(value)):
                setattr(self, name, value)

    def del_attrs(self, *attr_names) -> None:
        '''
        Delete attributes from the object.

        This method is responsible for deleting a series of attributes provided in the
        *args format, which means attribute names in the form of strings.

        Parameters:
        ----------
        *attr_names : positional arguments
            Attributes to be deleted from the object.

        Returns:
        -------
        None.

        Examples:
        --------
        >>> flex_obj = FlexObject(developer='David Santana', github='davidsantana06')
        >>> hasattr(flex_obj, 'developer')
        True
        >>> flex_obj.del_attrs('developer')
        >>> hasattr(flex_obj, 'developer')
        False
        '''
        for name in attr_names:
            if (type(name) == str) and (hasattr(self, name)):
                delattr(self, name)

    @staticmethod
    def safe_json_types() -> Tuple[type]:
        '''
        Return a tuple of safe JSON-compatible data types.

        This static method returns a tuple of data types that are safe to use in JSON
        serialization and deserialization.

        Returns:
        -------
        Tuple[type]
            A tuple containing data types suitable for JSON representation.

        Examples:
        --------
        >>> safe_types = FlexObject.safe_json_types()
        >>> isinstance(None, safe_types)
        True
        >>> isinstance(42, safe_types)
        True
        >>> isinstance("Hello", safe_types)
        True
        >>> isinstance({}, safe_types)
        True
        '''
        return (
            NoneType,               # none/null
            bool, float, int, str,  # primitive variables
            dict, list, tuple       # data structures
        )

    def safe_json_attrs(self) -> Dict[str, Any]:
        """
        Return a dictionary of safe JSON-compatible attributes.

        This method returns a dictionary containing attribute names and values from
        the object that are safe for JSON serialization. Only attributes whose names
        do not start with an underscore ('_') and whose values have data types within
        the safe JSON types are included.

        Returns:
        -------
        Dict[str, Any]
            A dictionary containing attribute names and values suitable for JSON.

        Examples:
        --------
        >>> flex_obj = FlexObject(name='David Santana', _secret=77)
        >>> safe_attrs = flex_obj.safe_json_attrs()
        >>> bool('name' in safe_attrs)
        True
        >>> bool('_secret' in safe_attrs)
        False
        """
        return {
            name: value
            for name, value in self.__dict__.items()
            if (
                (not name.startswith('_')) and
                (type(value) in self.safe_json_types())
            )
        }

    def from_json(self, json_str: str) -> None:
        '''
        Initialize object attributes from a JSON string.

        This method initializes the object's attributes by loading them from a JSON
        string. The JSON data is expected to represent a dictionary of attribute names
        and values. The `set_attrs` method is then used to assign these attributes to
        the object.

        Parameters:
        ----------
        json_str : str
            A JSON-formatted string containing attribute data.

        Returns:
        -------
        None.

        Examples:
        --------
        >>> json_str = '{"name": "David Santana", "age": 21}'
        >>> flex_obj = FlexObject()
        >>> flex_obj.from_json(json_str)
        >>> flex_obj.name
        'David Santana'
        >>> flex_obj.age
        21
        '''
        attrs: Dict[str, Any] = json.load(json_str)
        self.set_attrs(**attrs)

    def to_json(self, indent: int = 4) -> str:
        '''
        Convert object attributes to a JSON-formatted string.

        This method converts the object's safe attributes into a JSON-formatted string.
        The attributes are obtained using the `safe_json_attrs` method. The resulting
        JSON string can be indented using the specified value for the 'indent' parameter.

        Parameters:
        ----------
        indent : int, optional
            The number of spaces used for indentation in the resulting JSON string.
            Default is 4.

        Returns:
        -------
        str
            A JSON-formatted string representing the object's safe attributes.

        Examples:
        --------
        >>> flex_obj = FlexObject(name='David Santana', age=21)
        >>> json_str = flex_obj.to_json()
        >>> print(json_str)
        {
            "name": "David Santana",
            "age": 21
        }
        '''
        data: Dict[str, Any] = self.safe_json_attrs()
        json_str: str = json.dumps(data, indent=indent)
        return json_str

    def read_json_file(self, file_path: str) -> None:
        '''
        Read and load object attributes from a JSON file.

        This method reads a JSON file located at the specified 'file_path' and loads
        its content as attributes for the object. The `set_attrs` method is then used
        to assign these attributes to the object.

        Parameters:
        ----------
        file_path : str
            The path to the JSON file containing attribute data.

        Returns:
        -------
        None.

        Examples:
        --------
        Let's assume the JSON file contains: {"name": "David Santana", "age": 21}
        >>> flex_obj = FlexObject()
        >>> flex_obj.read_json_file('../data.json')
        >>> flex_obj.name
        'David Santana'
        >>> flex_obj.age
        21
        '''
        with open(file_path, 'r') as json_file:
            attrs: Dict[str, Any] = json.load(json_file)
            self.set_attrs(**attrs)

    def write_json_file(self, file_path: str = '', indent: int = 4) -> None:
        '''
        Write object attributes to a JSON file.

        This method writes the object's safe attributes to a JSON file. If no 'file_path'
        is provided or if the provided 'file_path' does not have a ".json" extension, a
        default file name is generated based on the class name. The attributes are saved
        in JSON format using the specified 'indent' value for formatting.

        Parameters:
        ----------
        file_path : str, optional
            The path to the JSON file to be written. If not provided or does not end with
            '.json', a default name based on the class name is used.
        indent : int, optional
            The number of spaces used for indentation in the resulting JSON file. Default
            is 4.

        Returns:
        -------
        None.

        Examples:
        --------
        >>> flex_obj = FlexObject(name='David Santana', age=21)
        >>> flex_obj.write_json_file('../data.json')
        # A JSON file 'data.json' is created with contents:
        # {
        #     "name": "David Santana",
        #     "age": 21
        # }
        '''
        if (not file_path) or (not file_path.endswith('.json')):
            file_path = join(
                abspath(dirname(__file__)),
                f'{self.__class__.__name__}.json'
            )
        attrs: Dict[str, Any] = self.safe_json_attrs()

        with open(file_path, 'w') as json_file:
            json.dump(attrs, json_file, indent=indent)
