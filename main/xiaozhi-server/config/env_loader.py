import os
import re
import sys
import yaml

_env_var_pattern = re.compile(r'\$\{([^}^{]+)\}')


def _resolve_env_var(match):
    name = match.group(1)
    value = os.environ.get(name)
    if value is None or value == '':
        print(f"Error: environment variable '{name}' is not set or empty", file=sys.stderr)
        sys.exit(1)
    return value


def _env_var_constructor(loader, node):
    return _env_var_pattern.sub(_resolve_env_var, node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!env_var', _env_var_pattern, None)
EnvVarLoader.add_constructor('!env_var', _env_var_constructor)
