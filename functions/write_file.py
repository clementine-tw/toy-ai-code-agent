import os


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
