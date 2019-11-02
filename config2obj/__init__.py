import json
import os
import yaml


def default(arg1):
    '''
    Sets a default value to a property if it is not present in
    configuration file.

    Can be a constant ("text", False, 123, []) or can be also a
    function (lambda : now())
    '''
    def default_decorator(func):
        def wrapper(self):
            try:
                return func(self)
            except KeyError:
                # default value can be also a callable
                if callable(arg1):
                    return arg1()
                return arg1
        return wrapper
    return default_decorator


def converter(arg1):
    '''
    Converts a value from a property according to the converter.
    The converter must be a callable object (like a lambda).

    If the value to apply the convert is a constant ("text", False, 123, [])
    the  apply it; if is a list, applyt he converter at each element
    on the list

    '''
    def converter_decorator(func):
        def wrapper(self):
            if not callable(arg1):
                raise Exception("Converter must be callable")

            val = func(self)
            if isinstance(val, list):
                return [arg1(v) for v in val]
            elif isinstance(val, (str, bool, int, float)) or val is None:
                return arg1(val)
            else:
                raise Exception("Invalid type to apply the converter")
        return wrapper
    return converter_decorator


class BasicConfigProperty():
    '''
    Basic config property.
    Every complex property should inherit from this class.
    '''

    def __init__(self, data):
        self._data = data

    def get(self, key):
        return self._data[key]


class BasicConfigObject(BasicConfigProperty):
    '''
    Basic config object.
    Every base config class should inherit from this class.
    '''

    def __init__(self, filename, ctype=None):
        self._filename = filename
        self._ctype = self._get_ctype(self._filename, ctype)
        super().__init__(self._load_data(self._filename, ctype))

    def _get_ctype(self, filename, ctype):
        if ctype is None:
            not_used, ctype = os.path.splitext(self._filename)
            return ctype[1:]

    def _load_data(self, filename, ctype):
        if self._ctype == "json":
            with open(filename, "r") as json_file:
                return json.load(json_file)
        elif self._ctype == "yaml":
            with open(filename, "r") as ymlfile:
                return yaml.load(ymlfile, Loader=yaml.FullLoader)

        raise Exception(f"{ctype} not supported")

