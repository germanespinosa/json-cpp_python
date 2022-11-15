import json_cpp2_core
import json_cpp2

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
        if value_type in [bool, int, float, str, list, tuple, set, dict, type(None)]:
            return True
        if issubclass(value_type, json_cpp2.JsonParsable):
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
        >>> from json_cpp2 import JsonObject
        >>> JsonParser.to_json(JsonObject(a=10,b=20))
        '{"a":10,"b":20}'
        >>> JsonParser.to_json({'a':10,'b':20})
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
            if value_type is None or not issubclass(value_type, json_cpp2.JsonObject):
                value = json_cpp2.JsonObject()
            else:
                value = value_type()
            value.__from_descriptor__(descriptor)
            return value
        elif type(descriptor) is json_cpp2_core.JsonListDescriptor:
            if value_type is None or not issubclass(value_type, json_cpp2.JsonList):
                value = json_cpp2.JsonList()
            else:
                value = value_type()
            value.__from_descriptor__(descriptor)
            return value

    @staticmethod
    def parse(json_string: str):
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
        variant_descriptor = json_cpp2_core.JsonVariantDescriptor()
        variant_descriptor.from_json(json_string)
        return JsonParser.__get_value__(variant_descriptor)

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
            return json_cpp2.JsonObject(**value)
        elif issubclass(value_type, json_cpp2.JsonParsable):
            return value.__get_descriptor__()
        elif hasattr(value, '__getitem__'):
            return json_cpp2.JsonList(iterable=value).__get_descriptor__()
        else:
            raise TypeError("type %s not supported by json-cpp" % str(value_type))

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
    def from_url(cls, *args, **kwargs):
        """
        Creates an instance of the corresponding type (None, bool, int, float, string, JsonObject or JsonList)
        and loads the values from an url containing a valid json string.

        :raises HTTPError: when failes to download content
        :param args: passed through to request.get (see https://www.w3schools.com/python/ref_requests_get.asp)
        :return: the value in its corresponding type
        :rtype: None, bool, int, float, string, JsonObject or JsonList
        :Example:
        >>> o = JsonParser.from_url("http://echo.jsontest.com/member1/value/member2/5")
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
        req = requests.get(*args, **kwargs)
        if req.status_code == 200:
            return cls.parse(req.text)
        else:
            req.raise_for_status()

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
