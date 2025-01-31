import os

def search_MixMHC2pred_path():
    """Search for a folder containing 'MixMHC2pred' at the same level as the 'script' folder."""
    # Get the directory of the current script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Traverse up to the parent directory of 'script'
    script_parent_dir = os.path.dirname(os.path.dirname(script_dir))

    # Search for directories with 'MixMHC2pred' in their name
    for item in os.listdir(script_parent_dir):
        item_path = os.path.join(script_parent_dir, item)
        if os.path.isdir(item_path) and "MixMHC2pred-" in item:
            return item_path

    return None

def validate_MixMHC2pred_path(path):
    """Validate if the provided path contains the required MixMHC2pred executable."""
    if not os.path.exists(path):
        print("The provided path does not exist.")
        return False

    # Check if the MixMHC2pred executable exists in the folder
    expected_file = os.path.join(path, "MixMHC2pred_unix")
    if not os.path.isfile(expected_file):
        print("The provided path exists but does not contain the MixMHC2pred executable.")
        return False

    return True

def find_or_prompt_MixMHC2pred_path():
    """Check the default location for MixMHC2pred; otherwise, prompt the user."""
    default_path = search_MixMHC2pred_path()

    if validate_MixMHC2pred_path(default_path):
        print(f"MixMHC2pred Found! Using default MixMHC2pred path: {default_path}")
        return default_path
    else:
        print("Default MixMHC2pred path not found or invalid.")

    # Prompt the user for a custom path
    while True:
        custom_path = input("Enter the full path to the MixMHC2pred folder: ").strip()
        if validate_MixMHC2pred_path(custom_path):
            return custom_path
        print("Invalid path. Please try again.")
