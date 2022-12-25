import click
import openai

from .constants import OPENAI_NUM_ANSWERS_MIN, OPENAI_TEMPERATURE_MIN, OPENAI_TEMPERATURE_MAX, OPENAI_MAX_TOKENS_MIN, \
    OPENAI_TOP_P_MIN, OPENAI_TOP_P_MAX, OPENAI_FREQUENCY_PENALTY_MIN, OPENAI_FREQUENCY_PENALTY_MAX, \
    OPENAI_PRESENCE_PENALTY_MIN, OPENAI_PRESENCE_PENALTY_MAX
from .utils import KeyHelper, ConfigHelper, PrintHelper, AvailableModels
from .entrypoint_config import config
from .entrypoint_init import init
from .entrypoint_key import key


class DefaultCommandGroup(click.Group):
    """
    Allows for both:
    * askai "<COMMAND>"
    * askai <GROUP> <COMMAND>

    Inspired from: https://stackoverflow.com/a/52069546
    """

    default_command: bool

    def command(self, *args, **kwargs):
        default_command = kwargs.pop('default_command', False)
        if default_command and not args:
            kwargs['name'] = kwargs.get('name', ' ')
        decorator = super(DefaultCommandGroup, self).command(*args, **kwargs)

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

    def format_help(self, ctx, formatter) -> None:
        PrintHelper.logo()
        PrintHelper.help_what_is_askai()
        PrintHelper.help_does_it_cost()
        PrintHelper.help_requirements()
        PrintHelper.help_main_command_options()
        PrintHelper.help_commands()


@click.group(cls=DefaultCommandGroup)
def askai() -> None:
    """"""
    pass


@askai.command(default_command=True)
@click.argument("prompt")
@click.option("-n", "--num-answers", type=click.IntRange(min=OPENAI_NUM_ANSWERS_MIN), help="Number of alternative answers")
@click.option("-m", "--model", type=click.Choice(choices=AvailableModels.members_as_list()), help="OpenAI model to use. E.g. `text-ada-001`")
@click.option("-t", "--temperature", type=click.FloatRange(min=OPENAI_TEMPERATURE_MIN, max=OPENAI_TEMPERATURE_MAX), help="Temperature")
@click.option("--max-tokens", type=click.IntRange(min=OPENAI_MAX_TOKENS_MIN), help="Max tokens")
@click.option("--top-p", type=click.FloatRange(min=OPENAI_TOP_P_MIN, max=OPENAI_TOP_P_MAX), help="Top p")
@click.option("--frequency-penalty", type=click.FloatRange(min=OPENAI_FREQUENCY_PENALTY_MIN, max=OPENAI_FREQUENCY_PENALTY_MAX), help="Frequency penalty")
@click.option("--presence-penalty", type=click.FloatRange(min=OPENAI_PRESENCE_PENALTY_MIN, max=OPENAI_PRESENCE_PENALTY_MAX), help="Presence penalty")
def ask(prompt: str,
        num_answers: int,
        model: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float) -> None:
    openai.api_key = KeyHelper.from_file()
    _config = ConfigHelper.from_file()

    response = openai.Completion.create(
        model=model if model else _config.model,
        prompt=prompt,
        temperature=temperature if temperature else _config.temperature,
        max_tokens=max_tokens if max_tokens else _config.max_tokens,
        n=num_answers if num_answers else _config.num_answers,
        top_p=top_p if top_p else _config.top_p,
        frequency_penalty=frequency_penalty if frequency_penalty else _config.frequency_penalty,
        presence_penalty=presence_penalty if presence_penalty else _config.presence_penalty
    )
    PrintHelper.print_response(response=response)


askai.add_command(init)
askai.add_command(config)
askai.add_command(key)
