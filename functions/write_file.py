import os
from google.genai import types


def write_file(working_dir, file_path, content):
    target_path = os.path.abspath(os.path.join(working_dir, file_path))
    if not target_path.startswith(os.path.abspath(working_dir)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(target_path):
            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error writing file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrite the file if it exists, or create the file and write content if not exists, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to overwrite, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file.",
            ),
        },
    ),
)
