import click
import openai

from config_setup import Config
from constants import API_KEY_PATH, TIMEOUT_SEC
from entrypoint_config import config
from entrypoint_init import init
from entrypoint_key import key


class DefaultCommandGroup(click.Group):
    """allow a default command for a group"""

    def command(self, *args, **kwargs):
        default_command = kwargs.pop('default_command', False)
        if default_command and not args:
            kwargs['name'] = kwargs.get('name', ' ')
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

        click.echo("Does it cost anything?\n"
                   "  Yes (after the free quota is used).\n"
                   "\n"
                   "  askai is using your OpenAI API-key to generate the answers to your questions.\n"
                   "  When creating a new account at OpenAI, you will get $18 of requests for free.\n"
                   "  After you've consumed the free quota, you need to add payment info to your \n"
                   "  OpenAI account to continue to use askai.\n")

        click.echo("Requirements:\n"
                   "  * Create an OpenAI account and generate an API-key\n"
                   "  * Run 'askai init' to add you API key and setup the default config.\n")


@click.group(cls=DefaultCommandGroup)
def askai():
    """"""
    pass


@askai.command(default_command=True)
@click.option("-n", "--num-answers", type=int, help="Number of alternative answers")
@click.option("--model", type=str, help="OpenAI model to use. E.g. `text-ada-001`")
@click.option("--temperature", type=float, help="Temperature")
@click.option("--max-tokens", type=int, help="Max tokens")
@click.option("--top-p", type=float, help="Top p")
@click.option("--frequency_penalty", type=int, help="Frequency penalty")
@click.option("--presence_penalty", type=int, help="Presence penalty")
@click.argument("prompt")
def ask(prompt: str,
        num_answers: int,
        model: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float):
    openai.api_key = get_api_key()
    _config = Config.from_config_file()

    response = openai.Completion.create(
        model=model if model else _config.model,
        prompt=prompt,
        temperature=temperature if temperature else _config.temperature,
        max_tokens=max_tokens if max_tokens else _config.max_tokens,
        n=num_answers if num_answers else _config.num_answers,
        top_p=top_p if top_p else _config.top_p,
        frequency_penalty=frequency_penalty if frequency_penalty else _config.frequency_penalty,
        presence_penalty=presence_penalty if presence_penalty else _config.presence_penalty,
        timeout=1
    )
    print_response(response=response)


askai.add_command(init)
askai.add_command(config)
askai.add_command(key)


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
