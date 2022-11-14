import json_cpp2_core

from abc import abstractmethod
from random import choice
import string
from copy import copy, deepcopy


class MemberNotFoundError(Exception):
    def __init__(self, member_name: str):
        Exception.__init__(self, "member %s not found" % member_name)


class JsonParser:
    """
    Provides access to the json parsing and writing functionality.
    """

    @staticmethod
    def is_supported_type(value_or_type) -> bool:
        """
        Checks if a value or type is supported by json-cpp

        :param value_or_type: value or type to be checked
        :type value_or_type: any value or type
        :return: True if value or type is supported, False otherwise
        :rtype: bool
        :Example:

        >>> JsonParser.is_supported_type(None)
        True
        >>> JsonParser.is_supported_type(bool)
        True
        >>> JsonParser.is_supported_type(True)
        True
        >>> JsonParser.is_supported_type(False)
        True
        >>> JsonParser.is_supported_type(int)
        True
        >>> JsonParser.is_supported_type(5)
        True
        >>> JsonParser.is_supported_type(float)
        True
        >>> JsonParser.is_supported_type(object)
        False
        """
        if not type(value_or_type) is type:
            value_type = type(value_or_type)
        else:
            value_type = value_or_type
        if value_type in [bool, int, float, str, list, tuple, set, dict, JsonObject, JsonList, type(None)]:
            return True
        if issubclass(value_type, (JsonObject, JsonList)):
            return True
        return False

    @staticmethod
    def check_supported_type(value_or_type) -> None:
        """
        Raises an exception if value or type is not supported by json-cpp

        :param value_or_type: value or type to be checked
        :type value_or_type: any value or type
        :raises TypeError: when value or type is not supported
        :rtype: None
        :Example:

        >>> JsonParser.check_supported_type(None)
        >>> JsonParser.check_supported_type(bool)
        >>> JsonParser.check_supported_type(True)
        >>> JsonParser.check_supported_type(False)
        >>> JsonParser.check_supported_type(int)
        >>> JsonParser.check_supported_type(5)
        >>> JsonParser.check_supported_type(float)
        >>> JsonParser.check_supported_type("a string")
        >>> JsonParser.check_supported_type(object)
        Traceback (most recent call last):
         ...
        TypeError: type <class 'object'> is not supported
        """
        if not JsonParser.is_supported_type(value_or_type):
            if type(value_or_type) is type:
                value_type = value_or_type
            else:
                value_type = type(value_or_type)
            raise TypeError("type %s is not supported" % str(value_type))

    @staticmethod
    def __get_descriptor_type__(json_descriptor):
        if type(json_descriptor) is json_cpp2_core.JsonBoolDescriptor or \
                type(json_descriptor) is json_cpp2_core.JsonIntDescriptor or \
                type(json_descriptor) is json_cpp2_core.JsonFloatDescriptor or \
                type(json_descriptor) is json_cpp2_core.JsonStringDescriptor:
            return type(json_descriptor.value)
        elif type(json_descriptor) is json_cpp2_core.JsonObjectDescriptor:
            return JsonObject
        elif type(json_descriptor) is json_cpp2_core.JsonListDescriptor:
            return JsonList

    @staticmethod
    def to_json(value) -> str:
        """
        Converts any supported value to a valid json string

        :param value: value or type to be converted
        :type value: any supported type
        :return:
        :rtype: str
        :raises TypeError: when value or type is not supported
        :Example:

        >>> JsonParser.to_json(None)
        'null'
        >>> JsonParser.to_json(True)
        'true'
        >>> JsonParser.to_json([1,2,3,None])
        '[1,2,3,null]'
        >>> JsonParser.to_json((1,2,3,None))
        '[1,2,3,null]'
        >>> JsonParser.to_json(JsonObject(a=10,b=20))
        '{"a":10,"b":20}'
        """
        json_descriptor = JsonParser.__create_descriptor__(value)
        return str(json_descriptor)

    @staticmethod
    def __get_value__(descriptor, value_type=None):
        if type(descriptor) is json_cpp2_core.JsonVariantDescriptor:
            descriptor = descriptor.get_value()
        if type(descriptor) is json_cpp2_core.JsonBoolDescriptor or \
                type(descriptor) is json_cpp2_core.JsonIntDescriptor or \
                type(descriptor) is json_cpp2_core.JsonFloatDescriptor or \
                type(descriptor) is json_cpp2_core.JsonStringDescriptor:
            return descriptor.value
        elif type(descriptor) is json_cpp2_core.JsonObjectDescriptor:
            if value_type is None or not issubclass(value_type, JsonObject):
                value = JsonObject()
            else:
                value = value_type()
            value.__from_descriptor__(descriptor)
            return value
        elif type(descriptor) is json_cpp2_core.JsonListDescriptor:
            if value_type is None or not issubclass(value_type, JsonList):
                value = JsonList()
            else:
                value = value_type()
            value.__from_descriptor__(descriptor)
            return value

    @classmethod
    def parse(cls, json_string: str):
        """
        Parses a valid json string into the corresponding value type
        (None, bool, int, float, string, JsonObject or JsonList)

        :raises RuntimeError: when string cannot be parsed
        :param json_string: the string to be parsed
        :type json_string: str
        :return: the value in its corresponding type
        :rtype: None, bool, int, float, string, JsonObject or JsonList
        :Example:

        >>> JsonParser.parse('true')
        True
        >>> JsonParser.parse('[1,2,3]')
        [1, 2, 3]
        >>> JsonParser.parse('{"a":10,"b":20}').a == 10
        True
        >>> JsonParser.parse('{"a":10,"b":20}')['a'] == 10
        True
        """
        if cls == JsonParser:
            variant_descriptor = json_cpp2_core.JsonVariantDescriptor()
            variant_descriptor.from_json(json_string)
            return JsonParser.__get_value__(variant_descriptor)
        else:
            o = cls()
            o.load(json_string)
            return o

    @staticmethod
    def __create_descriptor__(value):
        if type(value) is type:
            value_type = value
            value = value_type()
        else:
            value_type = type(value)
        if value_type in [bool, int, float, str]:
            return json_cpp2_core.get_descriptor(value)
        elif value is None:
            return json_cpp2_core.JsonNullDescriptor()
        elif value_type is dict:
            return JsonObject(**value)
        elif issubclass(value_type, JsonParser):
            return value.__get_descriptor__()
        elif hasattr(value, '__getitem__'):
            return JsonList(iterable=value).__get_descriptor__()
        else:
            raise TypeError("type %s not supported by json-cpp" % str(value_type))

    @abstractmethod
    def __get_descriptor__(self):
        pass

    @abstractmethod
    def __from_descriptor__(self, json_descriptor):
        pass

    @staticmethod
    def to_file(value, file_path: str) -> None:
        """
        Saves the value to a file in json format

        :raises TypeError: if type of value is not supported
        :param value: value to be saved
        :type value: any supported value type
        :param file_path: path to the file
        :type file_path: str
        :rtype: None
        :Example:

        >>> JsonParser.to_file({'a':10, 'b':20}, 'data.json')
        >>> open('data.json','r').read()
        '{"a":10,"b":20}'
        """
        json_string = JsonParser.to_json(value)
        with open(file_path, "w") as f:
            f.write(json_string)

    @classmethod
    def from_file(cls, file_path: str):
        """
        Creates an instance of the corresponding type (None, bool, int, float, string, JsonObject or JsonList)
        and loads the values from a file containing a valid json string.

        :param file_path: path to  the file
        :type file_path: str
        :return: the value in its corresponding type
        :rtype: None, bool, int, float, string, JsonObject or JsonList
        :Example:

        >>> open('data.json','w').write('{"a":10,"b":20}')
        15
        >>> o = JsonParser.from_file("data.json")
        >>> print(o.a)
        10
        >>> print(o.b)
        20
        """
        from os import path
        if not path.exists(file_path):
            raise FileNotFoundError("file %s not found" % file_path)
        json_content = ""
        with open(file_path) as f:
            json_content = f.read()
        return cls.parse(json_content)

    @classmethod
    def from_url(cls, uri: str):
        """
        Creates an instance of the corresponding type (None, bool, int, float, string, JsonObject or JsonList)
        and loads the values from an url containing a valid json string.

        :raises HTTPError: when failes to download content
        :param uri: path to  the file
        :type uri: str
        :return: the value in its corresponding type
        :rtype: None, bool, int, float, string, JsonObject or JsonList
        :Example:
        >>> o = JsonParser.from_url("https://raw.githubusercontent.com/germanespinosa/cellworld_data/master/test.json")
        >>> print(o.member1)
        value
        >>> print(o.member2)
        5
        >>> o = JsonParser.from_url("https://bad.url/test.json")
        Traceback (most recent call last):
        ...
        requests.exceptions.ConnectionError: HTTPSConnectionPool(host='bad.url', port=443): ...
        """
        import requests
        req = requests.get(uri)
        if req.status_code == 200:
            return cls.parse(req.text)
        else:
            req.raise_for_status()


class JsonList(list, JsonParser):
    """
    Provides json translation for iterable types.
    """

    def __init__(self, list_type: type = None, iterable = None, allow_null_values: bool = True):
        if list_type and not isinstance(list_type, type):
            raise TypeError("list_type must be a type")

        if iterable and not hasattr(iterable, '__getitem__'):
            raise Exception("iterable must be an iterable")

        list.__init__(self)
        self._list_type = list_type
        self._allow_null_values = allow_null_values
        if iterable:
            for i in iterable:
                self.append(i)


        # Example:
        # IntList = JsonList(name:"IntList", list_type=int, iterable=[1,2,3], allow_null_values=True)
        # l = IntList()
        # l.load("[4,5,6]")
        # assert(l, [1,2,3,4,5,6])

    @staticmethod
    def create_class(name: str = None,
                     list_type: type = None,
                     iterable=None,
                     allow_null_values: bool = True) -> type:
        """
        Creates a new type with a JsonList specification

        :param name: name of the class to be created. if empty, an autogenerated name will be provided
        :type name:  str
        :param list_type: supported type. if empty, the list will allow elements from any supported type
        :type list_type: supported type
        :param iterable: initial values for every new instance of the class. if empty, the list will be initialized empty
        :type iterable: iterable
        :param allow_null_values: allows the list to hold null values. they will be translated to None. default is True
        :type allow_null_values: bool
        :return: the new type
        :rtype: type
        :Example:

        >>> IntList = JsonList.create_class(list_type=int, iterable=[1,2,3])
        >>> l = IntList()
        >>> l.append(4)
        >>> l
        [1, 2, 3, 4]
        >>> l.append("a string")
        Traceback (most recent call last):
         ...
        TypeError: value of wrong type: expected <class 'int'>, received <class 'str'>
        """
        if name is None:
            name = ''.join(choice(string.ascii_lowercase) for i in range(10))

        def __init__(self):
            JsonList.__init__(self,
                              list_type=list_type,
                              iterable=iterable,
                              allow_null_values=allow_null_values)
        return type(name, (JsonList,), {"__init__": __init__})

    def __get_descriptor__(self):
        json_descriptor = json_cpp2_core.JsonListDescriptor()
        json_descriptor.allow_null_values = self._allow_null_values
        if self._list_type:
            self._item_descriptor = JsonParser.__create_descriptor__(self._list_type)
            json_descriptor.set_item_descriptor(self._item_descriptor)
        for i in self:
            json_descriptor.__iadd__(JsonParser.__create_descriptor__(i))
        return json_descriptor

    def __from_descriptor__(self, json_descriptor: json_cpp2_core.JsonListDescriptor):
        self.clear()
        for i in range(len(json_descriptor)):
            v = JsonParser.__get_value__(json_descriptor[i])
            self.append(v)

    def load(self, json_string: str) -> JsonParser:
        """
        Parses a json_string and loads the values into the list, validating type and nullability

        :param json_string: valid json string
        :return: the list itself

        """
        json_descriptor = self.__get_descriptor__()
        json_descriptor.from_json(json_string)
        self.__from_descriptor__(json_descriptor)
        return self

    def __type_check__(self, value):
        if value is None:
            if not self._allow_null_values:
                raise RuntimeError("list cannot contain null values when allow_null_values is set to false")
        elif self._list_type and not isinstance(value, self._list_type):
            raise TypeError("value of wrong type: expected %s, received %s" % (str(self._list_type), str(type(value))))
        JsonParser.check_supported_type(value)

    def append(self, item) -> None:
        """
        Validates type and nullability and adds the element to the list

        :raises TypeError: when item is of the wrong type
        :raises RuntimeError: when item is null and allow_null_values is set to False
        :param item: value to be added to the list
        :type item: any

        :return: None
        :rtype: None
        :Example:

        >>> l = JsonList(int, allow_null_values=False)
        >>> l.append(1)
        >>> l.append(2)
        >>> l.append(3)
        >>> print(l)
        [1,2,3]
        """
        self.__type_check__(item)
        list.append(self, item)

    def to_file(self, file_path: str) -> None:
        """
        Saves the list to a file in json format

        :param file_path: path to the file
        :type file_path: str
        :rtype: None
        :Example:

        >>> l = JsonList(int)
        >>> l.append(1)
        >>> l.append(2)
        >>> l.append(3)
        >>> l.to_file("data.json")
        >>> open('data.json','r').read()
        '[1,2,3]'
        """
        JsonParser.to_file(self, file_path)

    def __iadd__(self, other):
        for item in other:
            self.append(item)
        return self

    def __add__(self, other):
        new_list = JsonList(list_type=self._list_type, iterable=self)
        for item in other:
            new_list.append(item)
        return new_list

    def __radd__(self, other):
        new_list = JsonList(list_type=self._list_type, iterable=other)
        for item in self:
            new_list.append(item)
        return new_list

    def __str__(self):
        return str(self.__get_descriptor__())

    def __setitem__(self, key, value):
        self.__type_check__(value)
        list.__setitem__(self, key, value)

    def __setslice__(self, i, j, iterable):
        for index, value in enumerate(iterable):
            self.__setitem__(index + i, value)

    def get(self, member_name_or_lambda) -> JsonParser:
        """
        Selects a member from an object or executes a lambda on every element of the list.
        The lambda should return a value of a supported type

        :param member_name_or_lambda: if type is string, the values in the list must be objects, and they must contain an element with that name
        :type member_name_or_lambda: str or lambda
        :return: a JsonList with the results
        :rtype: JsonList

        """
        if type(member_name_or_lambda) is str:
            member_name = member_name_or_lambda
            if not issubclass(self._list_type, JsonObject):
                raise TypeError("get can only be used with json_object list types")

            o = self._list_type()
            if member_name not in o.keys():
                raise MemberNotFoundError(member_name)

            new_list = JsonList(type(o[member_name]))
            for i in self:
                new_list.append(i[member_name])
            return new_list
        else:
            if callable(member_name_or_lambda):
                process = member_name_or_lambda
                new_list = None
                for item in self:
                    result = process(item)
                    if new_list is None:
                        new_list = JsonList(type(result))
                    new_list.append(result)
                return new_list
            else:
                raise TypeError("incorrect parameter: expected member name or callable")

    def select(self, member_names) -> JsonParser:
        """
        Creates a list of objects with new objects of a new type containing a subset of the members from the originals

        :param member_names: list of member to be included in the new list
        :type member_names: list of str
        :return: the new list of objects of the new type
        :rtype: JsonList

        """
        if not issubclass(self._list_type, JsonObject):
            raise TypeError("select can only be used with json_object list types")

        new_list = None
        if self._list_type is not JsonObject:
            new_class_fields = dict()
            new_object = self._list_type()
            for member_name in member_names:
                new_class_fields[member_name] = new_object[member_name]
            new_list = JsonList(JsonObject.create_class(**new_class_fields))
        else:
            if len(self) == 0:
                new_list = JsonList(JsonObject)
            else:
                new_class_fields = dict()
                for member_name in member_names:
                    new_class_fields[member_name] = self[0][member_name]
                new_list = JsonList(JsonObject.create_class(**new_class_fields))

        for i in self:
            o = new_list._list_type()
            for member_name in member_names:
                o[member_name] = i[member_name]
            new_list.append(o)
        return new_list

    def where(self, lambda_criteria) -> JsonParser:
        """
        Creates a list with elements that passes a criteria

        :param lambda_criteria: lambda receiving each element and returning a bool
        :type lambda_criteria: lambda
        :return: the new list
        :rtype: JsonList

        """
        nl = JsonList(self._list_type)
        for i in self:
            if lambda_criteria(i):
                nl.append(i)
        return nl

    def __copy__(self):
        new_list = type(self)()
        new_list._list_type = self._list_type
        for item in self:
            new_list.append(item)
        return new_list

    def __deepcopy__(self, memo):
        new_list = type(self)()
        memo[id(self)] = new_list
        new_list._list_type = self._list_type
        for item in self:
            new_list.append(deepcopy(item))
        return new_list


class JsonObject(JsonParser):
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
            JsonParser.check_supported_type(value)
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
            _name = ''.join(choice(string.ascii_lowercase) for i in range(10))

        def __init__(self):
            JsonObject.__init__(self,
                                _mandatory_members=_mandatory_members,
                                _allow_undefined_members=_allow_undefined_members,
                                **kwargs)

        return type(_name, (JsonObject,), {"__init__": __init__})

    def __get_descriptor__(self):
        json_descriptor = json_cpp2_core.JsonObjectDescriptor()
        keys = self.keys()
        for key in keys:
            json_descriptor.add_member(key, JsonParser.__create_descriptor__(getattr(self, key)), key in self._mandatory_members)
        json_descriptor.allow_undefined_members = self._allow_undefined_members
        return json_descriptor

    def keys(self) -> JsonList:
        return JsonList(str, [key for key in vars(self) if key[0] != "_"])

    def __from_descriptor__(self, json_descriptor):
        members = json_descriptor.get_members()
        for member_name, member_descriptor in members:
            attr = getattr(self, member_name, None)
            value = JsonParser.__get_value__(member_descriptor, type(attr))
            setattr(self, member_name, value)

    def load(self, json_string: str) -> JsonParser:
        """
        Parses a json_string and loads the members into the object, validating type

        :param json_string: valid json string
        :return: the object itself

        """
        json_descriptor = self.__get_descriptor__()
        json_descriptor.from_json(json_string)
        self.__from_descriptor__(json_descriptor)
        return self

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
        JsonParser.to_file(self, file_path)

    def __str__(self):
        return str(self.__get_descriptor__())

    def __iter__(self):
        return self.keys().__iter__()

    def __getitem__(self, member_name):
        return getattr(self, member_name, None)

    def __setitem__(self, member_name, value):
        JsonParser.check_supported_type(value)
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
        new_object = type(self)()
        memo[id(self)] = new_object
        for key in self.keys():
            new_object[key] = deepcopy(self[key], memo)
        return new_object


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
