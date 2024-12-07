from ...configure.schema_gen import schema, LINE_BREAK


class Sh:

    def __init__(self, name: str, content: str | dict):
        if isinstance(content, str):
            self.command = content
            self.env = None
        else:
            script = content.get(schema.functions.sh_f.script.__str__)
            if not isinstance(script, str):
                raise Exception(
                    f"expected {schema.functions.sh_f.script.__str__} to be a string"
                )
            self.command = script

            env = content.get(schema.functions.sh_f.env.__str__)
            if env is not None:
                if not isinstance(env, dict):
                    raise Exception(
                        f"expected {schema.functions.sh_f.env.__str__} to be a dict"
                    )

                self.env = env

        self.name = name

    def render(self):
        return f"""(pkgs.writeScript \"{self.name}.sh\" ''
#!/usr/bin/env bash
{ LINE_BREAK.join([f'export {key}={value}' for key, value in self.env.items()]) if self.env is not None else ""}

{self.command}
'')"""
