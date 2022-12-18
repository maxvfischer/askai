import click

from config_setup import SetupHelper


@click.group()
def config():
    """Handle your config."""
    pass


@config.group()
def update():
    """Update your config"""


@update.command("all", help="Interface to update the full default config")
def update_all() -> None:
    setup_helper = SetupHelper()
    setup_helper.print_update_config_note()
    click.echo("-> STEP 1 - SET MODEL")
    setup_helper.user_input_model()
    click.echo("-> STEP 2 - SET NUMBER OF ALTERNATIVE ANSWERS GENERATED PER QUESTION")
    setup_helper.user_input_num_answers()
    click.echo("-> STEP 3 - SET MAXIMUM NUMBER OF TOKENS")
    setup_helper.user_input_max_token()
    click.echo("-> STEP 4 - SET TEMPERATURE")
    setup_helper.user_input_temperature()
    click.echo("-> STEP 5 - SET TOP_P")
    setup_helper.user_input_top_p()
    click.echo("-> STEP 6 - SET FREQUENCY PENALTY")
    setup_helper.user_input_frequency_penalty()
    click.echo("-> STEP 7 - SET PRESENCE PENALTY")
    setup_helper.user_input_presence_penalty()
    setup_helper.save_config()


@update.command("model", help="Update model")
def update_model() -> None:
    setup_helper = SetupHelper()
    click.echo(f"Update model")
    setup_helper.user_input_model()


@config.command(help="Reset the config to default")
def reset() -> None:
    setup_helper = SetupHelper()

    user_verification = input("Do you want to reset your config to the default values? [y/Y]? ")

    if user_verification.lower() in ["y", "yes"]:
        setup_helper.save_default_config()
    else:
        click.echo("Config not reset. Aborted!")


@config.command(help="Show current config")
def show() -> None:
    setup_helper = SetupHelper()
    setup_helper.show_config()
