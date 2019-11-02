# config2obj
Convert a config file into an object

This library provides a functionality to parses and convert a configuration file into an object (the result of the file read should be a dict - ex: JSON, YAML). This allows to change (if need) the value of the configuration, set defaults values if the value does not exists or validate if the configuration file has all the required information.

### Example
Image the configuration file is the following:
````json
{
    "mysql":{
        "user":"root",
        "passwd":"my secret password",
        "db":"prod"
    },
    "other":{
        "preprocessing_queue":[
            "preprocessing.scale_and_center",
            "preprocessing.dot_reduction",
            "preprocessing.connect_lines"
            ],
        "use_anonymous":false
    }
}
````
The corresponding objects in python are:
````python
class DatabaseConfig(BasicConfigProperty):
    @property
    @default("0.0.0.0")
    def host(self):
        return super().get("host")

    @property
    def user(self):
        return super().get("user")

    @property
    @converter(lambda x: x + "_salt")
    def passwd(self):
        return super().get("passwd")

    @property
    @converter(lambda x: str(x).upper())
    @default("DEV")
    def db(self):
        return super().get("db")


class OtherInfoConfig(BasicConfigProperty):
    @property
    @converter(lambda x: x + "_{$i}")
    @default([])
    def preprocessing_queue(self):
        return super().get("preprocessing_queue")

    @property
    @default(True)
    def use_anonymous(self):
        return super().get("use_anonymous")


class AppConfig(BasicConfigObject):
    @property
    def mysql(self):
        return DatabaseConfig(super().get("mysql"))

    @property
    def other(self):
        return OtherInfoConfig(super().get("other"))
````

The root object is `AppConfig` must inherits from `BasicConfigObject` that is the class responsible to load the file.
For each *complex* object it is need to create a class, in this case it is need to create a class for ***mysql*** and ***other*** property. These classes mst inherits from BasicConfigProperty.

Then for each attribute it can be set two properties: ***default*** and ***converter***.

### Default
When an atribute has this property and this key does not exist in the confuguration file, after the parse, it is assigned to this attribute a default value that is passed on the ***default*** property.

This value can be a constant (text, int, bool, ...) or can be also a function where the default value will be computed before being used.

##### Example:
```python
@default(0)
@default("default value")
@default(True)
@default([])
@default(lambda : now())
```

### Converter
It is also possible change the value of a property to guarantee consistency for instance., like for example, the environment name must be always upper case.

A function to convert the value must be passed into the ***converter*** property.

##### Example:
```python
@converter(lambda x : str(x).upper())
```








### TODO:
- Add more types of configuration