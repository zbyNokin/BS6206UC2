import os

def get_script_parent_dir():
    """Get the parent directory of the 'script' folder."""
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Traverse up the directory tree until the parent is 'script'
    while script_dir and os.path.basename(script_dir) != "script":
        script_dir = os.path.dirname(script_dir)

    # Return the parent directory of 'script'
    if script_dir and os.path.basename(script_dir) == "script":
        return os.path.dirname(script_dir)  # Parent of 'script'
    else:
        raise FileNotFoundError("Could not find the 'script' directory in the path.")

def get_default_annovar_path():
    """Get the default path assuming 'annovar' is at the same level as the 'script' folder."""
    try:
        script_parent_dir = get_script_parent_dir()
        default_path = os.path.join(script_parent_dir, "annovar")  # Parent of 'script' + 'annovar'
        return default_path
    except FileNotFoundError as e:
        print(e)
        return None

def validate_path(path):
    """Validate if the path exists and contains expected ANNOVAR files."""
    if not os.path.exists(path):
        print("The provided path does not exist.")
        return False

    # Check for specific files like 'convert2annovar.pl' to confirm it's an ANNOVAR directory
    expected_file = os.path.join(path, "convert2annovar.pl")
    if not os.path.isfile(expected_file):
        print("The provided path exists but does not contain the expected ANNOVAR files.")
        return False

    return True

def find_or_prompt_annovar_path():
    """Check the default location, otherwise prompt the user."""
    default_path = get_default_annovar_path()

    if default_path and validate_path(default_path):
        print(f"Founded! Using default ANNOVAR path: {default_path}")
        return default_path
    else:
        print("Default ANNOVAR path not found or invalid.")

    # Prompt the user for a custom path
    while True:
        custom_path = input("Enter the full path to the ANNOVAR folder: ").strip()
        if validate_path(custom_path):
            return custom_path
        print("Invalid path. Please try again.")
