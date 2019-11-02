# config2obj
Convert a config file into an object

This library provides a functionality to parses and convert a configuration file (this file should be read as a dict - JSON, YAML) into an object. This allows to change (if need) the value of the configuration, set defaults values if the value does not exists or validate if the configuration file has all the required information.

For that a schema must be difined.

### Schema
The schema is composed by terminal values, an objects and an arrays.

|  Property | Type | Description  |
| ------------ | ------------ | ------------ |
|   mandatory |  Boolean | If is not defined or if is true, the property is mandatory. If is not mandatory, this value must be set to False. |
| default  |  Simple value (like string, int, float, ...) or lambda  | Is the property is not mandatory a default value can be set. This can be a constant value or a function to compute the value|
|  converter | lambda function   | If it is defined, passes the value to the function and computes the new value of the property; if is not defined return the value it self |
| type |  Available values: object, array | Defines this property as a complex and can defines an object or an array. If this property is defined , the above properties are ignored (if they are present).  |
| childs |   | Defines the properties childs in case of the parent property be an object or an array. If it is an array, the content of the *child* property should be *mandatory*, *default* or *converter*; in case of an object the value should be a name of the sub-property  |
| empty | Boolean | In case of the property being an array, if it is True, the array can be empty; if it is False or not present, the array must have values |

### Example
````python
schema = {
    "property1": {
        "type": "object",
        "childs": {
            "key1": {
                "mandatory": True,
                "converter": lambda x: str(x).upper()
            },
            "key2": {},
            "key3": {
                "mandatory": False,
                "default": lambda: "default_value_3"
            },
            "superkey": {
                "type": "object",
                "childs": {
                    "superkey1": {
                        "converter": lambda x: str(x)[4:-1]
                    }
                }
            }
        }
    },
    "property2": {
        "type": "object",
        "childs": {
            "array1": {
                "type": "array",
                "empty": False,
                "childs": {
                    "converter": lambda x: "array 1 key: " + str(x)
                }
            },
            "array2": {
                "type": "array",
                "empty": True,
                "childs": {
                    "converter": lambda x: "array 2 key: " + str(x)
                }
            }
        }
    }
}
````
This schema validates the next JSON config file:

```json
{
    "property1": {
        "key1": "value1",
        "key2": "value2",
        "superkey": {
            "superkey1": "supervalue1"
        }
    },
    "property2": {
        "array1": [
            "arrvalue1",
            "arrvalue2",
            "arrvalue3"
        ],
        "array2": []
    }
}
```
### TODO:
- Add more types of configuration