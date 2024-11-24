from ...configure.schema_gen import schema, LINE_BREAK


class Sh:

    def __init__(self, name: str, content: str | dict):
        if isinstance(content, str):
            self.command = content
            self.env = None
        else:
            script = content.get(schema.sh.script.__str__)
            if not isinstance(script, str):
                raise Exception(f"expected {schema.sh.script.__str__} to be a string")
            self.command = script

            env = content.get(schema.sh.env.__str__)
            if env is not None:
                if not isinstance(env, list):
                    raise Exception(f"expected {schema.sh.env.__str__} to be a list")

                self.env = env

        self.name = name

    def render(self):
        return f"""(pkgs.writeScript \"{self.name}.sh\" ''
#!/usr/bin/env bash
{ LINE_BREAK.join([f'export {env}' for env in self.env]) if self.env is not None else ""}

{self.command}
'')"""
