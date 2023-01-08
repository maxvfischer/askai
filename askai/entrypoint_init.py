from pathlib import Path

import click

from .constants import CONFIG_PATH, API_KEY_PATH
from .utils import KeyHelper, ConfigHelper, PrintHelper


@click.command()
def init() -> None:
    """Initialize askai."""
    _init()


def _init(config_path: Path = CONFIG_PATH, api_key_path: Path = API_KEY_PATH) -> None:
    """Separate function for testing"""
    PrintHelper.logo()

    key_helper = KeyHelper()
    PrintHelper.key()
    key_helper.input()
    key_helper.save(api_key_path=api_key_path)

    config_helper = ConfigHelper()
    config_helper.reset(config_path=config_path)

    click.echo("Initialization done!")
