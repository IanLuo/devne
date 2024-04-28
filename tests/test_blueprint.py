from ss.configure.blueprint import *


class TestBlueprint:
    def test_parse_yaml(self, config: str):
        assert isinstance(dict, parse_yaml(config))


if __name__ == "__main__":
    # read config from test.yaml
    with open("tests/test.yaml", "r") as f:
        config = f.read()

    TestBlueprint().test_parse_yaml(config)
