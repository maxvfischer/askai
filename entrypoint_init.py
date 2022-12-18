import click

from config_setup import SetupHelper


@click.command()
def init() -> None:
    """Initialize askai."""
    setup_helper = SetupHelper()
    setup_helper.print_logo()
    setup_helper.user_input_api_key()
    setup_helper.save_api_key()
    setup_helper.save_default_config()
    click.echo("Initialization done!")
