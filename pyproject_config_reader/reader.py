import os
import platform
import stat
from pathlib import Path

import jmespath as jp
import yaml
from dotenv import load_dotenv

load_dotenv('project.env')


def running_under_jupyter():
    import os
    return bool(os.environ.get('JPY_SESSION_NAME'))


def get_config(node_path: str, *, conf_string_delimiter: str = None, strict: bool = True, **kwargs):
    config_file = Path(
        os.getenv('CONFIG_PATH')
    ).expanduser().resolve()

    assert (
               not os.stat(config_file).st_mode & (stat.S_IWOTH | stat.S_IWGRP | stat.S_IRGRP | stat.S_IROTH)
           ) or platform.system() == 'Windows', 'Check config file permissions'

    assert config_file.exists(), f'No config file {config_file.as_posix()}'

    if isinstance(
            config := jp.search(
                node_path,
                yaml.full_load(
                    config_file.read_bytes(),
                )
            ),
            dict
    ):
        config = config | kwargs
    elif config is None and not strict:
        return

    assert config, f'No config found for {node_path}'

    if conf_string_delimiter is None or not isinstance(config, dict):
        return config

    return str(conf_string_delimiter).join(f'{k}={v}' for k, v in config.items())


__all__ = [
    'get_config',
    'running_under_jupyter'
]
