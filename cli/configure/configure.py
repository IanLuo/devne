from .parser import parse 
from file_generator.unit import Unit

class Configure:
    def __init__(self, configStr):
        self._config = parse(configStr)

    @property
    def language(self) -> str:
        return self._config["sdk"]["language"]


    @property
    def version(self) -> str:
        return self._config["sdk"]["version"]

    @property
    def sdkPackagesDefault(self) -> list[str]:
        return self._config["sdk"]["packages"]["default"]

    @property
    def sdkPackagesDev(self) -> list[str]:
        return self._config["sdk"]["packages"]["development"]

    @property
    def dependenciesDefault(self) -> list[str]:
        return self._config["dependencies"]["default"]


    @property
    def dependenciesDev(self) -> list[str]:
        return self._config["dependencies"]["development"]

    @property
    def units(self) -> list[Unit]:
        return self._config["units"].map(lambda unit: Unit(unit))

    @property
    def ref(self) -> str:
        return self._config["ref"]
