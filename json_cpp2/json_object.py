import json_cpp2
import json_cpp2_core

class JsonObject(json_cpp2.JsonParsable):
    """
    Provides json translation for objects.
    """

    def __init__(self, _mandatory_members: list = None, _allow_undefined_members: bool = True, **kwargs):
        if _mandatory_members:
            self._mandatory_members = _mandatory_members
        else:
            self._mandatory_members = list()

        self._allow_undefined_members = _allow_undefined_members
        for key, value in kwargs.items():
            json_cpp2.JsonParser.check_supported_type(value)
            if type(value) is type:
                setattr(self, key, value())
            else:
                setattr(self, key, value)

    @staticmethod
    def create_class(_name: str = None,
                     _mandatory_members: list = None,
                     _allow_undefined_members: bool = True,
                     **kwargs) -> type:
        """
        Creates a new type with a JsonObject specification

        :param _name: (optional) name of the class to be created. if empty, an autogenerated name will be provided
        :param _mandatory_members: list of strings containing the names of the mandatory members
        :param _allow_undefined_members: boolean. default True. allows additional members to be added during parsing
        :param kwargs: list of members and values
        :return: the new type
        """
        if _name is None:
            from string import ascii_lowercase
            from random import choice
            _name = ''.join(choice(ascii_lowercase) for i in range(10))

        def __init__(self):
            JsonObject.__init__(self,
                                _mandatory_members=_mandatory_members,
                                _allow_undefined_members=_allow_undefined_members,
                                **kwargs)

        return type(_name, (JsonObject,), {"__init__": __init__})

    def select(self, member_names: list):
        '''
        creates a new JsonObject with a subset of members from the original object

        :param member_names: list of members names to be included in the new object
        :type member_names: list of str
        :return: the new JsonObject
        :rtype: JsonObject
        :Example:
        >>> c3 = JsonObject(x=10,y=20,z=30)
        >>> c3.select(("x","y"))
        {"x":10,"y":20}
        '''
        d = dict()
        for member in member_names:
            d[member] = self[member]
        return JsonObject(**d)

    def __get_descriptor__(self):
        json_descriptor = json_cpp2_core.JsonObjectDescriptor()
        keys = self.keys()
        for key in keys:
            json_descriptor.add_member(key, json_cpp2.JsonParser.__create_descriptor__(getattr(self, key)), key in self._mandatory_members)
        json_descriptor.allow_undefined_members = self._allow_undefined_members
        return json_descriptor

    def keys(self) -> list:
        '''
        List of member names defines in the object

        :return: the list of member names
        :rtype: JsonList(str)
        :Example:
        >>> JsonObject(x=10,y=20).keys()
        ['x', 'y']
        '''
        return [key for key in vars(self) if key[0] != "_"]

    def __from_descriptor__(self, json_descriptor):
        members = json_descriptor.get_members()
        for member_name, member_descriptor in members:
            attr = getattr(self, member_name, None)
            value = json_cpp2.JsonParser.__get_value__(member_descriptor, type(attr))
            setattr(self, member_name, value)
        return self

    def load(self, json_string: str) -> json_cpp2.JsonParsable:
        """
        Parses a json_string and loads the members into the object, validating type

        :param json_string: valid json string
        :return: the object itself
        :rtype: JsonObject
        :Example:
        >>> c = JsonObject(x=int, y=int)
        >>> c.load('{"x":10,"y":20}')
        {"x":10,"y":20}
        """
        json_descriptor = self.__get_descriptor__()
        json_descriptor.from_json(json_string)
        self.__from_descriptor__(json_descriptor)
        return self

    def format(self, format_string: str) -> str:
        '''
        Creates a formatted string using the values of the objects and a format specification

        :param format_string: format specification
        :type format_string: str (see https://www.w3schools.com/python/ref_string_format.asp)
        :return: the formatted string
        :rtype: str
        :Example:
        >>> c = JsonObject(x=10, y=20)
        >>> c.format("'x' is equal to {x} and 'y' is equal to {y}")
        "'x' is equal to 10 and 'y' is equal to 20"
        >>> p = JsonObject(name="John", address=JsonObject(street="oak", number=1876))
        >>> p.format("{name} lives in {address.number} {address.street}")
        'John lives in 1876 oak'
        >>> f = JsonObject(x = 10.0 / 3.0, pos=2)
        >>> f.format("x={x:.2f} in position {pos:04d}")
        'x=3.33 in position 0002'
        '''
        v = vars(self)
        for k in v:
            if not isinstance(v[k], JsonObject):
                continue
            pos = format_string.find("{%s:" % k)
            if pos >= 0:
                sub_format_start = format_string.find(":", pos) + 1
                sub_format_end = sub_format_start
                bracket_count = 1
                while bracket_count and sub_format_end < len(format_string):
                    c = format_string[sub_format_end]
                    if c == '{':
                        bracket_count += 1
                    if c == '}':
                        bracket_count -= 1
                    sub_format_end += 1
                sub_format = format_string[sub_format_start:sub_format_end-1]
                sub_str = v[k].format(sub_format)
                format_string = format_string[:pos] + sub_str + format_string[sub_format_end:]
        return format_string.format(**vars(self))

    def to_file(self, file_path: str) -> None:
        """
        Saves the list to a file in json format

        :param file_path: path to the file
        :type file_path: str
        :rtype: None
        :Example:
        >>> o = JsonObject(a=10, b=20)
        >>> o.to_file('object_data.json')
        >>> open('object_data.json', 'r').read()
        '{"a":10,"b":20}'
        """
        json_cpp2.JsonParser.to_file(self, file_path)

    def __str__(self):
        return str(self.__get_descriptor__())

    def __repr__(self):
        return str(self.__get_descriptor__())


    def __iter__(self):
        return self.keys().__iter__()

    def __getitem__(self, member_name):
        return getattr(self, member_name, None)

    def __setitem__(self, member_name, value):
        json_cpp2.JsonParser.check_supported_type(value)
        current = self[member_name]
        if current is not None:
            if not isinstance(value, type(current)):
                raise TypeError("value of wrong type: expected %s, received %s" % (str(type(current)), str(type(value))))
        setattr(self, member_name, value)

    def __eq__(self, other):
        keys = self.keys()
        for k in keys:
            if not other[k] == self[k]:
                return False
        return True

    def __copy__(self):
        new_object = type(self)()
        for key in self.keys():
            new_object[key] = self[key]
        return new_object

    def __deepcopy__(self, memo):
        from copy import deepcopy
        new_object = type(self)()
        memo[id(self)] = new_object
        for key in self.keys():
            new_object[key] = deepcopy(self[key], memo)
        return new_object


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
