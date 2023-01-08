from pathlib import Path

import click

from .utils import KeyHelper, PrintHelper
from .constants import API_KEY_PATH


@click.group()
def key():
    """Update or remove your API key."""
    pass


@key.command()
def add() -> None:
    """Add API key"""
    _add()


def _add(api_key_path: Path = API_KEY_PATH) -> None:
    """Separate function for testing"""
    if API_KEY_PATH.is_file():
        PrintHelper.key_exists()

    key_helper = KeyHelper()
    key_helper.input()
    key_helper.save(api_key_path=api_key_path)


@key.command()
def remove() -> None:
    """Remove your stored API key"""
    _remove()


def _remove(api_key_path: Path = API_KEY_PATH) -> None:
    """Separate function for testing"""
    if not API_KEY_PATH.is_file():
        PrintHelper.no_key()
    else:
        user_verification = input("Do you want to remove your API key? [y/Y]? ")
        if user_verification.lower() in ["y", "yes"]:
            KeyHelper().remove(api_key_path=api_key_path)
        else:
            click.echo("API key not removed.")
