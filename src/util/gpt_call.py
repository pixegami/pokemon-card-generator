from functools import cached_property
import os
from dotenv import load_dotenv
import openai
from retry import retry


class OpenAIClient:

    SINGLETON_CLIENT = None

    @cached_property
    def is_openai_enabled(self):
        print("Checking for OpenAI API key...")
        load_dotenv()
        print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
        if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
            # Print warning message in red.
            print(
                "\033[91m"
                + "WARNING: OpenAI API key not found. OpenAI will not be used."
                + "\033[0m"
            )
            return False
        else:
            return True

    @retry(tries=3, delay=3.0)
    def get_completion(self, prompt: str, max_tokens: int = 128, n: int = 1):
        return "No OpenAI API key found."
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


def gpt_client():
    if OpenAIClient.SINGLETON_CLIENT is None:
        OpenAIClient.SINGLETON_CLIENT = OpenAIClient()
    return OpenAIClient.SINGLETON_CLIENT
