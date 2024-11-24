from typing import Any, Dict
import re
from dataclasses import dataclass, field
from schema import raw_keys


def sanitize_name(name: str) -> str:
    """Convert a string to a valid Python class/variable name."""
    # Replace other special characters with underscore
    name = re.sub(r"[^0-9a-zA-Z_>]", "_", name)
    if name[0].isdigit():
        name = f"_{name}"
    if name.endswith(">"):
        name = name.replace(">", "_f")
    return name


def generate_class_code(data: Dict[str, Any], class_name: str = "Config") -> str:
    """Generate a nested class structure from a dictionary."""

    lines = [f"@dataclass(frozen=True)"]
    lines.append(f"class {class_name}:")
    class_definitions = []
    class_attributes = []

    class_attributes.append(
        f"""
    @property
    def __str__(self):
        return '{
        class_name[0].lower() + class_name[1:-2] + ">" if class_name.endswith("_f")  else  class_name[0].lower() + class_name[1:]
        }'
        """
    )

    for key, value in data.items():
        attr_name = sanitize_name(key)

        if isinstance(value, dict):
            nested_class_name = attr_name.capitalize()
            nested_class = generate_class_code(value, nested_class_name)
            class_definitions.append(nested_class)
            class_attributes.append(
                f"    {attr_name}: {nested_class_name} = {nested_class_name}()"
            )
        elif isinstance(value, list):
            class_attributes.append(
                f"    {attr_name}: list = field(default_factory=lambda: {repr(value)})"
            )
        elif isinstance(value, str):
            class_attributes.append(f"    {attr_name}: str = {repr(value)}")
        elif isinstance(value, bool):
            class_attributes.append(f"    {attr_name}: bool = {value}")
        elif isinstance(value, int):
            class_attributes.append(f"    {attr_name}: int = {value}")
        elif isinstance(value, float):
            class_attributes.append(f"    {attr_name}: float = {value}")
        elif value is None:
            class_attributes.append(f"    {attr_name}: Any = None")

    if not class_attributes:
        lines.append("    pass")
    else:
        lines.extend(class_attributes)

    return "\n".join(class_definitions + [""] + lines)


def generate_code(data: Dict[str, Any], output_file: str = None) -> str:
    """Generate Python code with nested constant classes from a dictionary."""
    code = [
        'LINE_BREAK = "\\n"',
        'SPACE = " "',
        "from typing import Any",
        "from dataclasses import dataclass, field",
        "",
        generate_class_code(data),
        "schema = Config()",
    ]

    final_code = "\n".join(code)

    if output_file:
        with open(output_file, "w") as f:
            f.write(final_code)

    return final_code


# Example usage:
if __name__ == "__main__":

    content = generate_code(raw_keys)

    with open("ss/configure/schema_gen.py", "w") as f:
        f.write(content)
