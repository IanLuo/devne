LINE_BREAK = "\n"
SPACE = " "
from typing import Any
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Script:

    @property
    def __str__(self):
        return 'script'
        
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Env:

    @property
    def __str__(self):
        return 'env'
        
    _value_type: str = 'dict'
    _is_optional: bool = True

@dataclass(frozen=True)
class Sh_f:

    @property
    def __str__(self):
        return 'sh>'
        
    script: Script = Script()
    env: Env = Env()

@dataclass(frozen=True)
class Action_f:

    @property
    def __str__(self):
        return 'action>'
        

@dataclass(frozen=True)
class Url_f:

    @property
    def __str__(self):
        return 'url>'
        

@dataclass(frozen=True)
class File_f:

    @property
    def __str__(self):
        return 'file>'
        

@dataclass(frozen=True)
class Read_file_f:

    @property
    def __str__(self):
        return 'read_file>'
        

@dataclass(frozen=True)
class Git_f:

    @property
    def __str__(self):
        return 'git>'
        

@dataclass(frozen=True)
class Service_f:

    @property
    def __str__(self):
        return 'service>'
        

@dataclass(frozen=True)
class Functions:

    @property
    def __str__(self):
        return 'functions'
        
    sh_f: Sh_f = Sh_f()
    action_f: Action_f = Action_f()
    url_f: Url_f = Url_f()
    file_f: File_f = File_f()
    read_file_f: Read_file_f = Read_file_f()
    git_f: Git_f = Git_f()
    service_f: Service_f = Service_f()

@dataclass(frozen=True)
class Source:

    @property
    def __str__(self):
        return 'source'
        
    _value_type: str = 'str | url> | git> | read_file>'
    _is_optional: bool = False

@dataclass(frozen=True)
class Onstart:

    @property
    def __str__(self):
        return 'onstart'
        
    _value_type: str = 'list(sh> | action>)'
    _is_optional: bool = True

@dataclass(frozen=True)
class Actions:

    @property
    def __str__(self):
        return 'actions'
        
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Doc:

    @property
    def __str__(self):
        return 'doc'
        
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Units:

    @property
    def __str__(self):
        return 'units'
        
    _value_type: str = 'dict'
    _is_optional: bool = True
    source: Source = Source()
    onstart: Onstart = Onstart()
    actions: Actions = Actions()
    doc: Doc = Doc()

@dataclass(frozen=True)
class Path:

    @property
    def __str__(self):
        return 'path'
        
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Url:

    @property
    def __str__(self):
        return 'url'
        
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Ref:

    @property
    def __str__(self):
        return 'ref'
        
    _value_type: str = 'str'
    _is_optional: bool = True

@dataclass(frozen=True)
class Callable:

    @property
    def __str__(self):
        return 'callable'
        
    _value_type: str = 'bool'
    _is_optional: bool = True

@dataclass(frozen=True)
class Includes:

    @property
    def __str__(self):
        return 'includes'
        
    _value_type: str = 'dict'
    _is_optional: bool = True
    path: Path = Path()
    url: Url = Url()
    ref: Ref = Ref()
    callable: Callable = Callable()

@dataclass(frozen=True)
class Name:

    @property
    def __str__(self):
        return 'name'
        
    _value_type: str = 'str'
    _is_optional: bool = False

@dataclass(frozen=True)
class Version:

    @property
    def __str__(self):
        return 'version'
        
    _value_type: str = 'str'
    _is_optional: bool = False

@dataclass(frozen=True)
class Description:

    @property
    def __str__(self):
        return 'description'
        
    _value_type: str = 'str'
    _is_optional: bool = False

@dataclass(frozen=True)
class Metadata:

    @property
    def __str__(self):
        return 'metadata'
        
    _is_optional: bool = True
    _value_type: str = 'dict'
    name: Name = Name()
    version: Version = Version()
    description: Description = Description()

@dataclass(frozen=True)
class Actions:

    @property
    def __str__(self):
        return 'actions'
        
    _value_type: str = 'list(sh> | action>)'
    _is_optional: bool = True

@dataclass(frozen=True)
class Onstart:

    @property
    def __str__(self):
        return 'onstart'
        
    _value_type: str = 'list(sh> | action>)'
    _is_optional: bool = True

@dataclass(frozen=True)
class Env:

    @property
    def __str__(self):
        return 'env'
        
    _is_optional: bool = True
    _value_type: str = 'dict'

@dataclass(frozen=True)
class Depends_on:

    @property
    def __str__(self):
        return 'depends_on'
        
    _is_optional: bool = True
    _value_type: str = 'service'

@dataclass(frozen=True)
class Services:

    @property
    def __str__(self):
        return 'services'
        
    _value_type: str = 'dict'
    _is_optional: bool = True
    env: Env = Env()
    depends_on: Depends_on = Depends_on()

@dataclass(frozen=True)
class Config:

    @property
    def __str__(self):
        return 'config'
        
    pre_defined: list = field(default_factory=lambda: ['source', 'onstart', 'actions', 'listner', 'doc'])
    functions: Functions = Functions()
    units: Units = Units()
    includes: Includes = Includes()
    metadata: Metadata = Metadata()
    actions: Actions = Actions()
    onstart: Onstart = Onstart()
    services: Services = Services()
schema = Config()