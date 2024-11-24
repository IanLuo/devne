from typing import Any
from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    _value_type: str = 'str | url> | git> | read_file>'
    _is_optional: bool = False

@dataclass(frozen=True)
class Onstart:
    _value_type: str = 'list(sh> | action>)'
    _is_optional: bool = True

@dataclass(frozen=True)
class Actions:
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Doc:
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Units:
    _value_type: str = 'dict'
    _is_optional: bool = True
    source: Source
    onstart: Onstart
    actions: Actions
    doc: Doc

@dataclass(frozen=True)
class Path:
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Url:
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Ref:
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Include:
    _value_type: str = 'dict'
    _is_optional: bool = True
    path: Path
    url: Url
    ref: Ref

@dataclass(frozen=True)
class Name:
    _value_type: str = 'str'
    _is_optional: bool = False

@dataclass(frozen=True)
class Version:
    _value_type: str = 'str'
    _is_optional: bool = False

@dataclass(frozen=True)
class Description:
    _value_type: str = 'str'
    _is_optional: bool = False

@dataclass(frozen=True)
class Metadata:
    _is_optional: bool = True
    _value_type: str = 'dict'
    name: Name
    version: Version
    description: Description

@dataclass(frozen=True)
class Actions:
    _value_type: str = 'list(sh> | action>)'
    _is_optional: bool = True

@dataclass(frozen=True)
class Onstart:
    _value_type: str = 'list(sh> | action>)'
    _is_optional: bool = True

@dataclass(frozen=True)
class Env:
    _is_optional: bool = True
    _value_type: str = 'dict'

@dataclass(frozen=True)
class Depended_on:
    _is_optional: bool = True
    _value_type: str = 'service'

@dataclass(frozen=True)
class Services:
    _value_type: str = 'dict'
    _is_optional: bool = True
    env: Env
    depended_on: Depended_on

@dataclass(frozen=True)
class Config:
    units: Units
    include: Include
    metadata: Metadata
    actions: Actions
    onstart: Onstart
    services: Services