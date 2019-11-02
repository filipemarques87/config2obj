from config2obj import converter, default, BasicConfigProperty, BasicConfigObject


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


def test_json():
    conf = AppConfig("./test/test.json")
    assert conf.mysql.host == "0.0.0.0"
    assert conf.mysql.user == "root"
    assert conf.mysql.passwd == "my secret password_salt"
    assert conf.mysql.db == "PROD"

    assert not conf.other.use_anonymous
    assert conf.other.preprocessing_queue[0] == "preprocessing.scale_and_center_{$i}"
    assert conf.other.preprocessing_queue[1] == "preprocessing.dot_reduction_{$i}"
    assert conf.other.preprocessing_queue[2] == "preprocessing.connect_lines_{$i}"


def test_yaml():
    conf = AppConfig("./test/test.yaml")
    assert conf.mysql.host == "0.0.0.0"
    assert conf.mysql.user == "root"
    assert conf.mysql.passwd == "my secret password_salt"
    assert conf.mysql.db == "PROD"

    assert not conf.other.use_anonymous
    assert conf.other.preprocessing_queue[0] == "preprocessing.scale_and_center_{$i}"
    assert conf.other.preprocessing_queue[1] == "preprocessing.dot_reduction_{$i}"
    assert conf.other.preprocessing_queue[2] == "preprocessing.connect_lines_{$i}"