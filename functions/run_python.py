import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        response = subprocess.run(
            ["python3", target_path],
            timeout=30,
            capture_output=True,
            cwd=abs_working_dir,
        )

        output = ""
        if response.stdout:
            output += f"STDOUT: {response.stdout}\n"
        if response.stderr:
            output += f"STDERR: {response.stderr}\n"
        if response.returncode != 0:
            output += f"Process exited with code {response.returncode}\n"
        if output == "":
            output += "No output produced\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file by command python3 in subprocess, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run by command python3, relative to the working directory.",
            ),
        },
    ),
)
