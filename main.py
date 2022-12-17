import click
import openai
from pathlib import Path

import yaml

from config_setup import SetupHelper
from constants import API_KEY_PATH, CONFIG_PATH


class DefaultCommandGroup(click.Group):
    """allow a default command for a group"""
    def command(self, *args, **kwargs):
        default_command = kwargs.pop('default_command', False)
        if default_command and not args:
            kwargs['name'] = kwargs.get('name', '<>')
        decorator = super(
            DefaultCommandGroup, self).command(*args, **kwargs)

        if default_command:
            def new_decorator(f):
                cmd = decorator(f)
                self.default_command = cmd.name
                return cmd

            return new_decorator

        return decorator

    def resolve_command(self, ctx, args):
        try:
            # test if the command parses
            return super(
                DefaultCommandGroup, self).resolve_command(ctx, args)
        except click.UsageError:
            # command did not parse, assume it is the default command
            args.insert(0, self.default_command)
            return super(
                DefaultCommandGroup, self).resolve_command(ctx, args)

    def format_usage(self, ctx, formatter):
        click.echo("██████████   ██████████   ███   ███  ██████████   ███\n"
                   "███    ███   ███    ███   ███  ███   ███    ███\n"
                   "███    ███   ███    ███   ███  ███   ███    ███\n"
                   "███    ███   ███    ███   ███▐███    ███    ███    ▄█\n"
                   "███    ███   ███          █████▀     ███    ███   ███\n"
                   "██████████   ██████████   █████      ██████████   ███▌\n"
                   "███    ███          ███   ███▐███    ███    ███   ███▌\n"
                   "███    ███          ███   ███  ███   ███    ███   ███\n"
                   "███    ███   ██████████   ███   ███  ███    ███   █▀\n"
                   "\n"
                   "    ~~~~~~~ Your simple terminal helper ~~~~~~~\n")

        click.echo("What is askai used for?\n"
                   "  askai gives you a simple CLI interface, integrated with the worlds\n"
                   "  most powerful and capable AI-models, OpenAI GPT3 models. This gives \n"
                   "  you the ability to interact with these models straight from your terminal.\n"
                   "\n"
                   "  Through askai, you're able to ask free-text questions and get the\n"
                   "  answers straight in your terminal.\n")

        click.echo("Required setup:\n"
                   "  To be able to use askai, you need to set up the connection with \n"
                   "  OpenAI. This is done through the following command: \n"
                   "  \n"
                   "    > askai addkey\n")


class CustomHelpOutput(click.Group):
    def format_usage(self, ctx, formatter):
        click.echo("██████████   ██████████   ███   ███  ██████████   ███\n"
                   "███    ███   ███    ███   ███  ███   ███    ███\n"
                   "███    ███   ███    ███   ███  ███   ███    ███\n"
                   "███    ███   ███    ███   ███▐███    ███    ███    ▄█\n"
                   "███    ███   ███          █████▀     ███    ███   ███\n"
                   "██████████   ██████████   █████      ██████████   ███▌\n"
                   "███    ███          ███   ███▐███    ███    ███   ███▌\n"
                   "███    ███          ███   ███  ███   ███    ███   ███\n"
                   "███    ███   ██████████   ███   ███  ███    ███   █▀\n"
                   "\n"
                   "    ~~~~~~~ Your simple terminal helper ~~~~~~~\n")

        click.echo("What is askai used for?\n"
                   "  askai gives you a simple CLI interface, integrated with the worlds\n"
                   "  most powerful and capable AI-models, OpenAI GPT3 models. This gives \n"
                   "  you the ability to interact with these models straight from your terminal.\n"
                   "\n"
                   "  Through askai, you're able to ask free-text questions and get the\n"
                   "  answers straight in your terminal.\n")

        click.echo("Required setup:\n"
                   "  To be able to use askai, you need to set up the connection with \n"
                   "  OpenAI. This is done through the following command: \n"
                   "  \n"
                   "    > askai addkey\n")


@click.group(cls=DefaultCommandGroup)
def askai():
    pass


@askai.command(help="Add API key")
def addkey() -> None:
    setup_helper = SetupHelper()
    setup_helper.print_logo()
    setup_helper.user_input_api_key()
    setup_helper.save_api_key()


@askai.command(help="Remove your stored API key")
def removekey() -> None:
    if not API_KEY_PATH.is_file():
        click.echo(click.style("No stored API key found.", fg="red"))
    else:
        API_KEY_PATH.unlink()
        click.echo(click.style("API key removed.", fg="green"))


@askai.command(help="Interface to update the default config of askai")
def updateconfig() -> None:
    setup_helper = SetupHelper()
    setup_helper.print_logo()
    setup_helper.print_update_config_note()
    setup_helper.user_input_model(step_num=1)
    setup_helper.user_input_num_answers(step_num=2)
    setup_helper.user_input_max_token(step_num=3)
    setup_helper.user_input_temperature(step_num=4)
    setup_helper.user_input_top_p(step_num=5)
    setup_helper.user_input_frequency_penalty(step_num=6)
    setup_helper.user_input_presence_penalty(step_num=7)
    setup_helper.save_config()


@askai.command(default_command=True)
@click.argument("prompt")
def ask_only_prompt(prompt: str):
    openai.api_key = get_api_key()
    default_config = get_default_config()

    response = openai.Completion.create(
        model=default_config["model"],
        prompt=prompt,
        temperature=default_config["temperature"],
        max_tokens=default_config["max_tokens"],
        n=default_config["num_answers"],
        top_p=default_config["top_p"],
        frequency_penalty=default_config["frequency_penalty"],
        presence_penalty=default_config["presence_penalty"]
    )
    print_response(response=response)

# @click.option("-p", "--prompt", type=str, help="Prompt.")
# @click.option("-n", "--num-answers", type=int, default=1, help="Number of alternative answers")
# @click.option("--model", type=str, default="text-davinci-003", help="OpenAI model to use. E.g. `text-ada-001`")
# @click.option("--temperature", type=float, default=0.4, help="Temperature")
# @click.option("--max-tokens", type=int, default=300, help="Max tokens")
# @click.option("--top-p", type=float, default=1.0, help="Top p")
# @click.option("--freq-penalty", type=int, default=0, help="Frequency penalty")
# @click.option("--pres-penalty", type=int, default=0, help="Presence penalty")
# @askai.command(default_command=True)
# def ask(prompt: str,
#           num_answers: int,
#           model: str,
#           temperature: float,
#           max_tokens: int,
#           top_p: float,
#           freq_penalty: int,
#           pres_penalty: int):
#     openai.api_key = get_api_key()
#     response = openai.Completion.create(
#         model=model,
#         prompt=prompt,
#         temperature=temperature,
#         max_tokens=max_tokens,
#         n=num_answers,
#         top_p=top_p,
#         frequency_penalty=freq_penalty,
#         presence_penalty=pres_penalty
#     )
#     print_response(response=response)
#
#


def get_default_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_api_key() -> str:
    with open(API_KEY_PATH, "r") as f:
        api_key = f.read().strip()
    return api_key


def print_response(response: openai.openai_object.OpenAIObject):
    if len(response["choices"]) == 1:
        print(response["choices"][0]["text"].lstrip("\n"))
    else:
        for idx, answer in enumerate(response["choices"]):
            print(f"### ANSWER {idx+1} ###")
            print(answer["text"].lstrip("\n"))
            print("\n")
