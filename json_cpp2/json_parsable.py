from abc import abstractmethod


class JsonParsable:

    _type_handlers = dict()
    _descriptor_handlers = dict()
    _descriptor_type = None
    @classmethod
    def __register_type_handler__(cls, types):
        if cls._descriptor_type is None:
            raise RuntimeError("JsonParsable class must have a defined a json descriptor")
        if types is tuple:
            for t in types:
                JsonParsable._type_handlers[t] = cls
        elif type(types) is type:
            JsonParsable._type_handlers[types] = cls

    @abstractmethod
    def __get_descriptor__(self):
        pass

    @abstractmethod
    def __from_descriptor__(self, json_descriptor):
        pass

    @classmethod
    def parse(cls, json_string):
        if cls is JsonParsable:
            raise RuntimeError()
        return cls().load(json_string)
