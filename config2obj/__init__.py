import json
import os


def _load_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def _get_default(attr):
    if "default" not in attr:
        return None
    elif callable(attr["default"]):
        return attr["default"]()
    else:
        return attr["default"]


def _convert(attr, val):
    if "converter" not in attr:
        return val
    elif callable(attr["converter"]):
        return attr["converter"](val)
    else:
        raise ValueError(f"'converter' for attribute must be callable")


def _get_value(name, data, schema):
    if name not in data:
        # madatory by default
        is_mandatory = "mandatory" not in schema or bool(schema["mandatory"])
        if is_mandatory:
            raise ValueError(f"key missing '{name}'")
        else:
            return _get_default(schema)
    else:
        return _convert(schema, data[name])


def _accept_empty(props):
    return "empty" in props and bool(props["empty"])

        # Creates a object from a dict


def _to_object(data, schema):
    attributes = {}
    for k, props in schema.items():
        if "type" in props:
            otype = props["type"]
            if otype == "object":
                attributes[k] = _to_object(data[k], props["childs"])
            elif otype == "array":
                if not _accept_empty(props) and len(data[k]) == 0:
                    raise ValueError(f"Array {k} cannot be empty")
                attributes[k] = [_convert(props["child"], value) for value in data[k]]
            else:
                raise ValueError(f"not recognize type: {otype}")
        else:
            # simple value (string, int, boolean, ...)
            attributes[k] = _get_value(k, data, props)

    # returns an object that represents the config
    return type("ConfigObject", (), attributes)()


def load(filename, schema, ctype=None):
    '''
    Loads the configuration from a file.
    The configuration type is deduced from the file extentions if the type variable is not defined.
    '''

    if ctype is None:
        not_used, ctype = os.path.splitext(filename)
        ctype = ctype[1:]

    data = None
    if ctype == "json":
        data = _load_json(filename)

    obj = _to_object(data, schema)
    return obj
