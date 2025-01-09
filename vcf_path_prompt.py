import os

def vcf_path_prompt():
    input_path = input("Please enter the full path to your VCF file: ")

    # Check if the file exists
    if not os.path.isfile(input_path):
        print("The file does not exist. Please check the path and try again.")
        return None

    # Print confirmation of the file path
    print(f"Your VCF file path is: {input_path}")
    return input_path
