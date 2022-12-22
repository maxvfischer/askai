import click

from .utils import ConfigHelper, PrintHelper


@click.group()
def config() -> None:
    """Handle your config."""
    pass


@config.command(help="Reset the config to default")
def reset() -> None:
    user_verification = input("Do you want to reset your config to the default values? [y/Y]? ")

    if user_verification.lower() in ["y", "yes"]:
        ConfigHelper().reset()
    else:
        click.echo("Config not reset. Aborted!")


@config.command(help="Show current config")
def show() -> None:
    ConfigHelper.show()


@config.group()
def update() -> None:
    """Update your config"""


@update.command("all", help="Interface to update the full default config")
def update_all() -> None:
    config_helper = ConfigHelper()
    PrintHelper.update_config()

    PrintHelper.step(step=1, description="SET MODEL")
    PrintHelper.model()
    config_helper.input_model()

    PrintHelper.step(step=2, description="SET NUMBER OF ALTERNATIVE ANSWERS GENERATED PER QUESTION")
    PrintHelper.num_answers()
    config_helper.input_num_answer()

    PrintHelper.step(step=3, description="SET MAXIMUM NUMBER OF TOKENS")
    PrintHelper.max_tokens()
    config_helper.input_max_token()

    PrintHelper.step(step=4, description="SET TEMPERATURE")
    PrintHelper.temperature()
    config_helper.input_temperature()

    PrintHelper.step(step=5, description="SET TOP_P")
    PrintHelper.top_p()
    config_helper.input_top_p()

    PrintHelper.step(step=6, description="SET FREQUENCY PENALTY")
    PrintHelper.frequency_penalty()
    config_helper.input_frequency_penalty()

    PrintHelper.step(step=7, description="SET PRESENCE PENALTY")
    PrintHelper.presence_penalty()
    config_helper.input_presence_penalty()

    config_helper.update()


@update.command(help="Update model")
def model() -> None:
    PrintHelper.model()
    config_helper = ConfigHelper.from_file()
    config_helper.input_model()
    config_helper.update()


@update.command(help="Update number of altenative answers generated per question")
def num_answers() -> None:
    PrintHelper.num_answers()
    config_helper = ConfigHelper.from_file()
    config_helper.input_num_answer()
    config_helper.update()


@update.command(help="Update maximum number of tokens")
def max_tokens() -> None:
    PrintHelper.max_tokens()
    config_helper = ConfigHelper().from_file()
    config_helper.input_max_token()
    config_helper.update()


@update.command(help="Update temperature")
def temperature() -> None:
    PrintHelper.temperature()
    config_helper = ConfigHelper().from_file()
    config_helper.input_temperature()
    config_helper.update()


@update.command(help="Update top_p")
def top_p() -> None:
    PrintHelper.top_p()
    config_helper = ConfigHelper().from_file()
    config_helper.input_top_p()
    config_helper.update()


@update.command(help="Update frequency penalty")
def frequency_penalty() -> None:
    PrintHelper.frequency_penalty()
    config_helper = ConfigHelper.from_file()
    config_helper.input_frequency_penalty()
    config_helper.update()


@update.command(help="Update presence penalty")
def presence_penalty() -> None:
    PrintHelper.presence_penalty()
    config_helper = ConfigHelper.from_file()
    config_helper.input_presence_penalty()
    config_helper.update()
