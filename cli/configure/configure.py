from .parser import parse 
from ..file_generator.unit import Unit
from typing import Optional

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
        def _get_unit(unit) -> Optional[Unit]:
            if type(unit) is str:
                return Unit(name=unit)
            elif type(unit) is dict:
                return Unit(json=unit)
            else:
                return None

        return [ value for value in map(lambda unit: _get_unit(unit), self._config["units"]) if value is not None ]

    @property
    def ref(self) -> str:
        return self._config["rev"]

