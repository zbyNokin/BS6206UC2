import os


def search_netMHCIIpan_path():
    """Search for a folder containing 'netMHCIIpan' at the same level as the 'script' folder."""
    # Get the directory of the current script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Traverse up to the parent directory of 'script'
    script_parent_dir = os.path.dirname(os.path.dirname(script_dir))

    # Search for directories with 'netMHCIIpan' in their name
    for item in os.listdir(script_parent_dir):
        item_path = os.path.join(script_parent_dir, item)
        if os.path.isdir(item_path) and "netMHCIIpan" in item:
            return item_path

    return None

def validate_netMHCIIpan_path(path):
    """Validate if the provided path contains the required netMHCIIpan executable."""
    if not os.path.exists(path):
        print("The provided path does not exist.")
        return False

    # Check if the netMHCIIpan executable exists in the folder
    expected_file = os.path.join(path, "netMHCIIpan")
    if not os.path.isfile(expected_file):
        print("The provided path exists but does not contain the netMHCIIpan executable.")
        return False

    return True

def find_or_prompt_netMHCIIpan_path():
    """Check the default location for netMHCIIpan; otherwise, prompt the user."""
    default_path = search_netMHCIIpan_path()

    if validate_netMHCIIpan_path(default_path):
        print(f"netMHCIIpan Found! Using default netMHCIIpan path: {default_path}")
        return default_path
    else:
        print("Default netMHCIIpan path not found or invalid.")

    # Prompt the user for a custom path
    while True:
        custom_path = input("Enter the full path to the netMHCIIpan folder: ").strip()
        if validate_netMHCIIpan_path(custom_path):
            return custom_path
        print("Invalid path. Please try again.")