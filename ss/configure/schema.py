from enum import Enum

K_IS_OPTIONAL = "_is_optional"
K_VALUE_TYPE = "_value_type"

raw_keys = {
    "pre-defined": ["source", "onstart", "actions", "listner", "doc"],
    "functions": {
        "sh>": {
            "script": {
                K_VALUE_TYPE: "str",
                K_IS_OPTIONAL: True,
            },
            "env": {
                K_VALUE_TYPE: "dict",
                K_IS_OPTIONAL: True,
            },
        },
        "action>": {},
        "url>": {},
        "file>": {},
        "read_file>": {},
        "git>": {},
        "service>": {},
    },
    "units": {
        K_VALUE_TYPE: "dict",
        K_IS_OPTIONAL: True,
        "source": {
            K_VALUE_TYPE: "str | url> | git> | read_file>",
            K_IS_OPTIONAL: False,
        },
        "onstart": {
            K_VALUE_TYPE: "list(sh> | action>)",
            K_IS_OPTIONAL: True,
        },
        "actions": {
            K_VALUE_TYPE: "str",
            K_IS_OPTIONAL: True,
        },
        "doc": {
            K_VALUE_TYPE: "str",
            K_IS_OPTIONAL: True,
        },
    },
    "includes": {
        K_VALUE_TYPE: "dict",
        K_IS_OPTIONAL: True,
        "path": {
            K_VALUE_TYPE: "str",
            K_IS_OPTIONAL: True,
        },
        "url": {
            K_VALUE_TYPE: "str",
            K_IS_OPTIONAL: True,
        },
        "ref": {
            K_VALUE_TYPE: "str",
            K_IS_OPTIONAL: True,
        },
        "callable": {
            K_VALUE_TYPE: "bool",
            K_IS_OPTIONAL: True,
        },
    },
    "metadata": {
        K_IS_OPTIONAL: True,
        K_VALUE_TYPE: "dict",
        "name": {
            K_VALUE_TYPE: "str",
            K_IS_OPTIONAL: False,
        },
        "version": {
            K_VALUE_TYPE: "str",
            K_IS_OPTIONAL: False,
        },
        "description": {
            K_VALUE_TYPE: "str",
            K_IS_OPTIONAL: False,
        },
    },
    "actions": {
        K_VALUE_TYPE: "list(sh> | action>)",
        K_IS_OPTIONAL: True,
    },
    "onstart": {
        K_VALUE_TYPE: "list(sh> | action>)",
        K_IS_OPTIONAL: True,
    },
    "services": {
        K_VALUE_TYPE: "dict",
        K_IS_OPTIONAL: True,
        "env": {
            K_IS_OPTIONAL: True,
            K_VALUE_TYPE: "dict",
        },
        "depends-on": {
            K_IS_OPTIONAL: True,
            K_VALUE_TYPE: "service",
        },
    },
}
