import click as click

from config_setup import SetupHelper
from constants import API_KEY_PATH


@click.group()
def key():
    """Update or remove your API key."""
    pass


@key.command()
def add() -> None:
    """Add API key"""
    setup_helper = SetupHelper()
    setup_helper.user_input_api_key()
    setup_helper.save_api_key()


@key.command()
def remove() -> None:
    """Remove your stored API key"""
    if not API_KEY_PATH.is_file():
        click.echo(click.style("No stored API key found.", fg="red"))
    else:
        user_verification = input("Do you want to remove your API key? [y/Y]? ")
        if user_verification.lower() in ["y", "yes"]:
            API_KEY_PATH.unlink()
            click.echo(click.style("API key removed.", fg="green"))
        else:
            click.echo("API key not removed.")