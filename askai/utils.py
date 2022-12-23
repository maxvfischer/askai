import yaml
import click
import openai
from getpass import getpass
from enum import Enum, auto
from typing import Callable
from dataclasses import dataclass, asdict
from openai.error import AuthenticationError
from openai.openai_object import OpenAIObject
from .constants import (
    CONFIG_PATH,
    API_KEY_PATH,
    DEFAULT_MODEL,
    DEFAULT_NUM_ANSWERS,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    DEFAULT_FREQUENCY_PENALTY,
    DEFAULT_PRESENCE_PENALTY, MAX_INPUT_TRIES
)


class AvailableModels(Enum):
    TEXT_ADA_001 = auto()
    TEXT_BABBAGE_001 = auto()
    TEXT_CURIE_001 = auto()
    TEXT_DAVINCI_003 = auto()

    @classmethod
    def as_list(cls) -> list:
        return list(map(lambda c: c.name.replace("_", "-").lower(), cls))


@dataclass
class ConfigHelper:
    model: str = DEFAULT_MODEL
    num_answers: int = DEFAULT_NUM_ANSWERS
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P
    frequency_penalty: float = DEFAULT_FREQUENCY_PENALTY
    presence_penalty: float = DEFAULT_PRESENCE_PENALTY

    @classmethod
    def from_file(cls) -> 'ConfigHelper':
        if CONFIG_PATH.is_file():
            with open(CONFIG_PATH, "r") as f:
                config = yaml.safe_load(f)
                return cls(**config)
        else:
            click.echo(click.style("No config file found, can't initialize config. "
                                    "Run 'askai config reset' to create a default config.", fg="red"))
            exit()

    def input_model(self) -> None:
        model = input("Choose model (1-4): ")
        num_of_tries = 1

        while not _is_int(model) or int(model) not in range(1, 5):
            if num_of_tries >= MAX_INPUT_TRIES:
                click.echo(click.style("Too many invalid tries. Aborted!", fg="red"))
                exit(1)

            click.echo(click.style("Choose value between 1 and 4.", fg="red"))
            model = input("Choose model (1-4): ")
            num_of_tries += 1

        self.model = AvailableModels(int(model)).name.replace("_", "-").lower()
        click.echo(click.style(f"Model chosen: {self.model}", fg="green"))
        click.echo()

    def input_num_answer(self) -> None:
        self.num_answers = self._input_integer(default_value=DEFAULT_NUM_ANSWERS, predicate=lambda x: x > 0)

    def input_max_token(self) -> None:
        self.max_tokens = self._input_integer(default_value=DEFAULT_MAX_TOKENS, predicate=lambda x: x > 0)

    def input_temperature(self) -> None:
        self.temperature = self._input_float(default_value=DEFAULT_TEMPERATURE, predicate=lambda x: 0.0 <= x <= 1.0)

    def input_top_p(self) -> None:
        self.top_p = self._input_float(default_value=DEFAULT_TOP_P, predicate=lambda x: 0.0 <= x <= 1.0)

    def input_frequency_penalty(self) -> None:
        self.frequency_penalty = self._input_float(
            default_value=DEFAULT_FREQUENCY_PENALTY,
            predicate=lambda x: -2.0 <= x <= 2.0
        )

    def input_presence_penalty(self) -> None:
        self.presence_penalty = self._input_float(
            default_value=DEFAULT_PRESENCE_PENALTY,
            predicate=lambda x: -2.0 <= x <= 2.0
        )

    def as_dict(self) -> dict:
        return asdict(self)

    def update(self) -> None:
        config = self.as_dict()
        with open(CONFIG_PATH, "w") as f:
            yaml.dump(config, f)

        click.echo(click.style("Config updated successfully!", fg="green"))

    @staticmethod
    def reset() -> None:
        config = ConfigHelper().as_dict()  # Create config with default values
        with open(CONFIG_PATH, "w") as f:
            yaml.dump(config, f)

        click.echo("\nDefault config has been created with the following values:")
        for key, value in config.items():
            click.echo(f"  * {key}={value}")
        click.echo(click.style("Successfully set config to default values\n", fg="green"))
        click.echo("To change the config, please see: 'askai config --help'\n")

    @staticmethod
    def show() -> None:
        if not CONFIG_PATH.is_file():
            click.echo("No config exists. Please reset the config ('askai config reset') "
                       "or see 'askai config --help'.\n")
        else:
            with open(CONFIG_PATH, "r") as f:
                try:
                    config = yaml.safe_load(f)
                    for key, value in config.items():
                        click.echo(f"{key}: {value}")
                except yaml.YAMLError:
                    click.echo("Something is wrong with the config. Please reset the config: 'askai config reset'")

    @staticmethod
    def _input_integer(default_value: int,
                       predicate: Callable[[int], bool] = lambda x: True) -> int:
        for _ in range(MAX_INPUT_TRIES):
            input_value = input(f"Choose (press enter for default = {default_value}): ")

            if input_value == "":
                click.echo(click.style(f"Value chosen: {default_value}", fg="green"))
                click.echo()
                return default_value

            if not _is_int(input_value):
                click.echo(click.style("Input is not an integer.\n", fg="red"))
                continue
            elif not predicate(int(input_value)):
                click.echo(click.style("Input is not within allowed range.\n", fg="red"))
                continue

            click.echo(click.style(f"Value chosen: {input_value}", fg="green"))
            click.echo()
            return int(input_value)

        click.echo(click.style("Too many invalid tries. Aborted!", fg="red"))
        exit(1)

    @staticmethod
    def _input_float(default_value: float,
                     predicate: Callable[[float], bool] = lambda x: True) -> float:
        for _ in range(MAX_INPUT_TRIES):
            input_value = input(f"Choose (press enter for default = {default_value}): ")

            if input_value == "":
                click.echo(click.style(f"Value chosen: {default_value}", fg="green"))
                click.echo()
                return default_value

            if not _is_float(input_value):
                click.echo(click.style("Input is not a float.\n", fg="red"))
                continue
            elif not predicate(float(input_value)):
                click.echo(click.style("Input is not within allowed range.\n", fg="red"))
                continue

            click.echo(click.style(f"Value chosen: {input_value}", fg="green"))
            click.echo()
            return float(input_value)

        click.echo(click.style("Too many invalid tries. Aborted!", fg="red"))
        exit(1)


@dataclass
class KeyHelper:
    api_key: str = ""

    def input(self) -> None:
        key = getpass("Enter API Key: ")
        num_tries = 1

        while not self._is_valid_api_key(key):
            if num_tries >= MAX_INPUT_TRIES:
                click.echo(click.style("Too many invalid tries. Aborted!", fg="red"))
                exit(1)
            click.echo(click.style("The API key is not valid.", fg="red"))
            key = getpass("Enter API Key: ")
            num_tries += 1

        self.api_key = key

    def save(self) -> None:
        API_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        API_KEY_PATH.write_text(self.api_key)
        click.echo(click.style("Your API key has been successfully added!", fg="green"))

    @staticmethod
    def remove() -> None:
        API_KEY_PATH.unlink()
        click.echo(click.style("API key removed.", fg="green"))

    @classmethod
    def from_file(cls) -> str:
        if API_KEY_PATH.is_file():
            with open(API_KEY_PATH, "r") as f:
                api_key = f.read().strip()
            return api_key
        else:
            click.echo(click.style("No API-key found, can't answer question. "
                                   "Please add a key ('askai key add') or initialize ('askai init').", fg="red"))
            exit()

    @staticmethod
    def _is_valid_api_key(key: str) -> bool:
        openai.api_key = key
        try:
            # Use free `content-filter-alpha` endpoint to check if API key is valid.
            openai.Completion.create(model="content-filter-alpha")
            return True
        except AuthenticationError:
            return False


class PrintHelper:

    @staticmethod
    def logo() -> None:
        click.echo("\n"
                   "██████████   ██████████   ███   ███  ██████████   ███\n"
                   "███    ███   ███    ███   ███   ███  ███    ███\n"
                   "███    ███   ███    ███   ███  ███   ███    ███\n"
                   "███    ███   ███    ███   ███▐███    ███    ███    ▄█\n"
                   "███    ███   ███          █████▀     ███    ███   ███\n"
                   "██████████   ██████████   █████▄     ██████████   ███▌\n"
                   "███    ███          ███   ███▐███    ███    ███   ███▌\n"
                   "███    ███          ███   ███  ███   ███    ███   ███\n"
                   "███    ███   ██████████   ███   ███  ███    ███   █▀\n"
                   "\n"
                   "    ~~~~~~~ Your simple terminal helper ~~~~~~~\n")

    @staticmethod
    def help_what_is_askai() -> None:
        click.echo("What is askai?\n"
                   "  askai is a simple CLI integration with the worlds most powerful \n"
                   "  and capable AI-model, OpenAI GPT3. This gives you the ability to \n"
                   "  interact with these models straight from your terminal.\n"
                   "\n"
                   "What can it be used for?\n"
                   "  askai enables you to ask any free-text question you want.\n"
                   "\n"
                   "  For example:\n"
                   "\n"
                   "    > askai \"What is the curl command to download html from a url?\"\n"
                   "    > askai \"How do you remove '\\n' from the beginning of a string using Python?\"\n"
                   "    > askai \"List the top 3 most common Python packages used to parse json-files\""
                   "\n")

    @staticmethod
    def help_does_it_cost() -> None:
        click.echo("Does it cost anything?\n"
                   "  Yes (after the free OpenAI quota is used).\n"
                   "\n"
                   "  askai is using your OpenAI API-key to generate the answers to your questions.\n"
                   "  When creating a new account at OpenAI, you will get $18 of requests for free.\n"
                   "  After you've consumed the free quota, you need to add payment info to your \n"
                   "  OpenAI account to continue to use askai.\n")
    
    @staticmethod
    def help_requirements() -> None:
        click.echo("Requirements:\n"
                   "  * Create an OpenAI account and generate an API-key\n"
                   "  * Run 'askai init' to add you API key and setup the default config.\n")

    @staticmethod
    def help_main_command_options() -> None:
        click.echo("Override config:\n"
                   "  askai \"<QUESTION>\" <OPTION> <VALUE>\n"
                   "\n"
                   "  --num-answers or -n\n"
                   "    Number of answers to generate. Note that more answers consume more tokens.\n"
                   "    Allowed values: >0\n"
                   "\n"
                   "  --model or -m\n"
                   "    Which model to use. See list of available models below.\n"
                   "\n"
                   "  --temperature or -t\n"
                   "    What sampling temperature to use. Higher value makes the model more \"creative\".\n"
                   "    Do not use at the same time as top-p.\n"
                   "    Allowed values: 0.0 <= temperature <= 1.0\n"
                   "\n"
                   "  --top-p"
                   "    What sampling nucleus to use. The model considers the results of the tokens with \n"
                   "    top_p probability mass. Do not use at the same time as temperature.\n"
                   "    Allowed values: 0.0 <= top_p <= 1.0\n"
                   "\n"
                   "  --max-tokens\n"
                   "    Maximum number of tokens used per question (incl. question + answer).\n"
                   "    Allowed values: >0\n"
                   "\n"
                   "  --frequency-penalty\n"
                   "    Positive values penalize new tokens based on whether they appear in the text so \n"
                   "    far, increasing the model's likelihood to talk about new topics.\n"
                   "    Allowed values: -2.0 <= frequency_penalty <= 2.0\n"
                   "\n"
                   "  --presence-penalty\n"
                   "    Positive values penalize new tokens based on their existing frequency in the text \n"
                   "    so far, decreasing the model's likelihood to repeat the same line verbatim.\n"
                   "    Allowed values: -2.0 <= presence_penalty <= 2.0\n"
                   "\n")

    @staticmethod
    def help_commands() -> None:
        click.echo("Commands:\n"
                   "  config  Handle your config.\n"
                   "  init    Initialize askai.\n"
                   "  key     Update or remove your API key.")
    
    @staticmethod
    def key() -> None:
        click.echo("To use the CLI, please enter your OpenAI API key. The key can be generated by \n"
                    "creating an account at https://openai.com/api/\n"
                    "\n"
                    "The key will only be stored locally in `~/.askai/key`.\n")

    @staticmethod
    def key_exists() -> None:
        click.echo("NOTE: You've already added a key. This old key will be overwritten in this setup!\n")

    @staticmethod
    def no_key() -> None:
        click.echo(click.style("No stored API key found.", fg="red"))

    @staticmethod
    def update_config() -> None:
        click.echo("NOTE: You're about to update the default config of askai. This will have an effect on "
                   "how the answers are generated. Make sure that you are well-informed around these effects. "
                   "You can read more here: https://beta.openai.com/docs/api-reference/completions/create\n")

    @staticmethod
    def step(step: int, description: str) -> None:
        click.echo(f"-> STEP {step} - {description}")

    @staticmethod
    def model() -> None:
        click.echo("   Different models have different capabilities.")
        for idx, model_name in enumerate(AvailableModels.as_list()):
            click.echo(f"   {idx+1}) {model_name}")

    @staticmethod
    def num_answers() -> None:
        click.echo("   This is the number of answers that will be displayed when you ask \n"
                   "   a question. A high number will use more tokens.\n\n"
                   "   Allowed values: >0\n")

    @staticmethod
    def max_tokens() -> None:
        click.echo("   Maximum number of tokens used, including question (prompt)\n"
                   "   and generated answers. A too low number might cut your answers shortly.\n\n"
                   "   Allowed values: >0\n")

    @staticmethod
    def temperature() -> None:
        click.echo("   Sampling temperature to use. Higher values means \n"
                   "   the model will take more risks. Try 0.9 for more \n"
                   "   creative applications, and 0 for ones with a well-defined \n"
                   "   answer.\n\n"
                   "   Allowed values: 0.0 <= temperature <= 1.0\n")

    @staticmethod
    def top_p() -> None:
        click.echo("   An alternative to sampling with temperature, called \n"
                   "   nucleus sampling, where the model considers the results \n"
                   "   of the tokens with top_p probability mass. So 0.1 means \n"
                   "   only the tokens comprising the top 10% probability mass \n"
                   "   are considered.\n"
                   "   It's generally recommend altering this or temperature, but not both!\n\n"
                   "   Allowed values: 0.0 <= top_p <= 1.0\n")

    @staticmethod
    def frequency_penalty() -> None:
        click.echo("   Positive values penalize new tokens based on their existing \n"
                   "   frequency in the text so far, decreasing the model's likelihood \n"
                   "   to repeat the same line verbatim.\n\n"
                   "   Allowed values: -2.0 <= frequency penalty <= 2.0\n")

    @staticmethod
    def presence_penalty() -> None:
        click.echo("   Positive values penalize new tokens based on whether they appear \n"
                   "   in the text so far, increasing the model's likelihood to talk about \n"
                   "   new topics.\n\n"
                   "   Allowed values: -2.0 <= presence penalty <= 2.0\n")

    @staticmethod
    def print_response(response: OpenAIObject) -> None:
        if len(response["choices"]) == 1:
            print(response["choices"][0]["text"].lstrip("\n"))
        else:
            for idx, answer in enumerate(response["choices"]):
                print(f"### ANSWER {idx+1} ###")
                print(answer["text"].lstrip("\n"))
                print("\n")


def _is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


def _is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
