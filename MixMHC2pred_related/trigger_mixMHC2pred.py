import os
import subprocess


def trigger_MixMHC2pred(mixmhc2pred_path, annovar_outputs_dir):
    """
    Function to trigger MixMHC2pred with the .pep file generated from ANNOVAR output.

    Parameters:
    - mixmhc2pred_path: Path to the MixMHC2pred executable.
    - annovar_outputs_dir: Path to the 'annovar_outputs' directory where .pep file is located.
    """
    # Validate MixMHC2pred path
    mixmhc2pred_executable = os.path.join(mixmhc2pred_path, "MixMHC2pred_unix")
    if not os.path.isfile(mixmhc2pred_executable):
        raise ValueError(f"MixMHC2pred executable not found in folder: {mixmhc2pred_path}")

    # Define the .pep file and validate its existence
    pep_file = os.path.join(annovar_outputs_dir, "mutated_peptide_sequences.pep")
    if not os.path.isfile(pep_file):
        raise FileNotFoundError(f"No file named 'mutated_peptide_sequences.pep' found in {annovar_outputs_dir}")

    # Create the MixMHC2pred_outputs folder
    base_dir = os.path.dirname(annovar_outputs_dir)  # Parent directory of annovar_outputs
    mixmhc2pred_outputs_dir = os.path.join(base_dir, "MixMHC2pred_outputs")
    os.makedirs(mixmhc2pred_outputs_dir, exist_ok=True)  # Create the folder if it doesn't exist

    # Locate the alleleList_mix.txt file in the script folder
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    allele_file_path = os.path.join(script_dir, "alleleList_mix.txt")
    if not os.path.isfile(allele_file_path):
        raise FileNotFoundError(f"No file named 'alleleList_mix.txt' found in the script folder: {script_dir}")

    # Read alleles from alleleList_mix.txt
    with open(allele_file_path, "r") as allele_file:
        alleles = [line.strip() for line in allele_file if line.strip()]  # Strip whitespace and ignore empty lines
    if not alleles:
        raise ValueError(
            "No alleles found in 'alleleList_mix.txt'. Please ensure the file contains valid allele entries.")

    # Convert alleles into space-separated format (instead of comma-separated like netMHCIIpan)
    alleles_str = " ".join(alleles)

    # Define the output file in the new directory
    output_file = os.path.join(mixmhc2pred_outputs_dir, "mutated_peptide_sequences_mix_out.txt")

    # Construct the MixMHC2pred command
    command = f"{mixmhc2pred_executable} -i {pep_file} -o {output_file} -a {alleles_str} --no_context"

    # Print and execute the command
    print(f"Executing MixMHC2pred command:\n{command}")
    subprocess.run(command, shell=True, check=True)

    print(f"MixMHC2pred prediction completed. Output saved to: {output_file}")
