import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt


def main():

    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("you must provide a prompt")
        exit(1)

    prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    print(generate_content(client, messages, verbose))


def generate_content(client, messages, verbose):

    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        if not response.function_calls:
            return response.text

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        for function_call_part in response.function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result = call_function(function_call_part, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("Error call function: {function_call_part}")
            messages.append(function_call_result)
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        if verbose:
            if response.usage_metadata is not None:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

    return "over 20 times"


if __name__ == "__main__":
    main()
