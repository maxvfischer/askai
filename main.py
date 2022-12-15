import os
import click
import openai


@click.command()
@click.option(
    "--prompt",
    "-p",
    type=str,
    required=True,
    help="Prompt to ask.",
)
@click.option(
    "--model",
    "-m",
    type=str,
    default="text-davinci-003",
    help="OpenAI model to use.",
)
@click.option(
    "--temp",
    "-t",
    type=float,
    default=0.4,
    help="Temperature",
)
@click.option(
    "--max-tokens",
    "-mt",
    type=int,
    default=300,
    help="Max tokens",
)
@click.option(
    "--num-answers",
    "-n",
    type=int,
    default=1,
    help="Number of alternative answers",
)
@click.option(
    "--top-p",
    type=float,
    default=1.0,
    help="Top p",
)
@click.option(
    "--freq-penalty",
    type=int,
    default=0,
    help="Frequency penalty",
)
@click.option(
    "--pres-penalty",
    type=int,
    default=0,
    help="Presence ppenalty",
)
def ask(prompt: str,
        model: str,
        temp: float,
        max_tokens: int,
        num_answers: int,
        top_p: float,
        freq_penalty: int,
        pres_penalty: int):

    openai.api_key = get_api_key()
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temp,
        max_tokens=max_tokens,
        n=num_answers,
        top_p=top_p,
        frequency_penalty=freq_penalty,
        presence_penalty=pres_penalty
    )
    print_response(response=response)


def get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        key_path = os.path.dirname(os.path.abspath(__file__)) + "/.key"
        with open(key_path, "r") as f:
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
