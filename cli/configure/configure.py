from .parser import parse 
from .unit import Unit
from typing import Optional

class Configure:
    def __init__(self, configStr):
        self._config = parse(configStr)

    @property
    def sdk_language(self) -> str:
        return self._config["sdk"]["language"]

    @property
    def sdk_version(self) -> str:
        return self._config["sdk"]["version"]

    @property
    def sdk_packages_default(self) -> list[str]:
        return self._config["sdk"]["packages"]["default"]

    @property
    def sdk_packages_dev(self) -> list[str]:
        return self._config["sdk"]["packages"]["development"]

    @property
    def dependencies_default(self) -> list[str]:
        return self._config["dependencies"]["default"]

    @property
    def dependencies_dev(self) -> list[str]:
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

    @property
    def name(self) -> str:
        return self._config["name"]

    @property
    def version(self) -> str:
        return self._config["version"]

    @property
    def description(self) -> str:
        return self._config["description"]
