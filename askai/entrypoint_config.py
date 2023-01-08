from pathlib import Path

import click

from .constants import CONFIG_PATH
from .utils import ConfigHelper, PrintHelper


@click.group()
def config() -> None:
    """Handle your config."""
    pass


@config.command(help="Reset the config to default")
def reset() -> None:
    _reset()


def _reset(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
    user_verification = input("Do you want to reset your config to the default values? [y/Y]? ")

    if user_verification.lower() in ["y", "yes"]:
        ConfigHelper().reset(config_path=config_path)
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
    _update_all()


def _update_all(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
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

    config_helper.update(config_path=config_path)


@update.command(help="Update model")
def model() -> None:
    _model()


def _model(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
    PrintHelper.model()
    config_helper = ConfigHelper.from_file()
    config_helper.input_model()
    config_helper.update(config_path=config_path)


@update.command(help="Update number of altenative answers generated per question")
def num_answers() -> None:
    _num_answers()


def _num_answers(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
    PrintHelper.num_answers()
    config_helper = ConfigHelper.from_file()
    config_helper.input_num_answer()
    config_helper.update(config_path=config_path)


@update.command(help="Update maximum number of tokens")
def max_tokens() -> None:
    _max_tokens()


def _max_tokens(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
    PrintHelper.max_tokens()
    config_helper = ConfigHelper().from_file()
    config_helper.input_max_token()
    config_helper.update(config_path=config_path)


@update.command(help="Update temperature")
def temperature() -> None:
    _temperature()


def _temperature(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
    PrintHelper.temperature()
    config_helper = ConfigHelper().from_file()
    config_helper.input_temperature()
    config_helper.update(config_path=config_path)


@update.command(help="Update top_p")
def top_p() -> None:
    _top_p()


def _top_p(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
    PrintHelper.top_p()
    config_helper = ConfigHelper().from_file()
    config_helper.input_top_p()
    config_helper.update(config_path=config_path)


@update.command(help="Update frequency penalty")
def frequency_penalty() -> None:
    _frequency_penalty()


def _frequency_penalty(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
    PrintHelper.frequency_penalty()
    config_helper = ConfigHelper.from_file()
    config_helper.input_frequency_penalty()
    config_helper.update(config_path=config_path)


@update.command(help="Update presence penalty")
def presence_penalty() -> None:
    _frequency_penalty()


def _presence_penalty(config_path: Path = CONFIG_PATH) -> None:
    """Separate function for testing"""
    PrintHelper.presence_penalty()
    config_helper = ConfigHelper.from_file()
    config_helper.input_presence_penalty()
    config_helper.update(config_path=config_path)
