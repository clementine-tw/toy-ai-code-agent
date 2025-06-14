import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        content = ""
        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)
        if len(content) >= MAX_CHARS:
            content += '[...File "{file_path}" truncated at 10000 characters]'
        return content

    except Exception as e:
        return f"Error reading file: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file which get content from, relative to the working directory.",
            ),
        },
    ),
)
