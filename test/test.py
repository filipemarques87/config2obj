import pytest

import config2obj

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
                "child": {
                    "converter": lambda x: "array 1 key: " + str(x)
                }
            },
            "array2": {
                "type": "array",
                "empty": True,
                "child": {
                    "converter": lambda x: "array 2 key: " + str(x)
                }
            }
        }
    }
}


def test_ok():
    conf = config2obj.load("test1.json", schema, ctype="json")
    assert str(type(conf)) == "<class 'config2obj.ConfigObject'>"
    assert str(type(conf.property1)) == "<class 'config2obj.ConfigObject'>"
    assert conf.property1.key1 == "VALUE1"
    assert conf.property1.key2 == "value2"
    assert conf.property1.key3 == "default_value_3"
    assert str(type(conf.property1.superkey)
               ) == "<class 'config2obj.ConfigObject'>"
    assert conf.property1.superkey.superkey1 == "rvalue"

    assert str(type(conf.property2)) == "<class 'config2obj.ConfigObject'>"
    assert isinstance(conf.property2.array1, list)
    assert len(conf.property2.array1) == 3
    assert conf.property2.array1[0] == "array 1 key: arrvalue1"
    assert conf.property2.array1[1] == "array 1 key: arrvalue2"
    assert conf.property2.array1[2] == "array 1 key: arrvalue3"
    assert isinstance(conf.property2.array2, list)
    assert len(conf.property2.array2) == 0


def test_empty_array():
    with pytest.raises(ValueError) as e:
        conf = config2obj.load("test2.json", schema, ctype="json")
    assert "Array array1 cannot be empty" == str(e.value)


def test_mandatory():
    with pytest.raises(ValueError) as e:
        conf = config2obj.load("test3.json", schema, ctype="json")
    assert "key missing 'key1'" == str(e.value)


def test_schema_1():
    schema = {
        "property1": {
            "type": "invalid",
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
                    "child": {
                        "converter": lambda x: "array 1 key: " + str(x)
                    }
                },
                "array2": {
                    "type": "array",
                    "empty": True,
                    "child": {
                        "converter": lambda x: "array 2 key: " + str(x)
                    }
                }
            }
        }
    }

    with pytest.raises(ValueError) as e:
        conf = config2obj.load("test1.json", schema, ctype="json")
    assert "not recognize type: invalid" == str(e.value)


def test_schema_2():
    schema = {
        "property1": {
            "type": "object",
            "childs": {
                "key1": {
                    "mandatory": True,
                    "converter": 3
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
                    "child": {
                        "converter": lambda x: "array 1 key: " + str(x)
                    }
                },
                "array2": {
                    "type": "array",
                    "empty": True,
                    "child": {
                        "converter": lambda x: "array 2 key: " + str(x)
                    }
                }
            }
        }
    }

    with pytest.raises(ValueError) as e:
        conf = config2obj.load("test1.json", schema, ctype="json")
    assert "'converter' for attribute must be callable" == str(e.value)
