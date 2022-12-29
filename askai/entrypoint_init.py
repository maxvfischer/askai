import click

from .utils import ConfigHelper, KeyHelper, PrintHelper


@click.command()
def init() -> None:
    """Initialize askai."""
    key_helper = KeyHelper()
    config_helper = ConfigHelper()
    PrintHelper.logo()

    PrintHelper.key()
    key_helper.input()
    key_helper.save()

    config_helper.reset()

    click.echo("Initialization done!")
