from functools import cached_property
import os
from dotenv import load_dotenv
import openai
from retry import retry


@retry(tries=3, delay=3.0)
def get_completion(prompt: str, max_tokens: int = 128, n: int = 1):

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.9,
        n=n,
    )
    return response


@cached_property
def is_openai_enabled():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None:
        # Print warning message in red.
        print(
            "\033[91m"
            + "WARNING: OpenAI API key not found. OpenAI will not be used."
            + "\033[0m"
        )
        return False
    else:
        return True
