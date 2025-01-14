import os
import subprocess


def trigger_netMHCIIpan(netmhciipan_path, annovar_outputs_dir):
    """
    Function to trigger NetMHCIIpan with the .pep file generated from ANNOVER output.

    Parameters:
    - netmhciipan_path: Path to the NetMHCIIpan executable.
    - annovar_outputs_dir: Path to the 'annovar_outputs' directory where .pep file is located.
    """
    # Validate NetMHCIIpan path
    netmhciipan_executable = os.path.join(netmhciipan_path, "netMHCIIpan")
    if not os.path.isfile(netmhciipan_executable):
        raise ValueError(f"NetMHCIIpan executable not found in folder: {netmhciipan_path}")

    # Define the .pep file and validate its existence
    pep_file = os.path.join(annovar_outputs_dir, "mutated_peptide_sequences.pep")
    if not os.path.isfile(pep_file):
        raise FileNotFoundError(f"No file named 'mutated_peptide_sequences.pep' found in {annovar_outputs_dir}")

    # Create the netMHCIIpan_outputs folder
    base_dir = os.path.dirname(annovar_outputs_dir)  # Parent directory of annovar_outputs
    netmhciipan_outputs_dir = os.path.join(base_dir, "netMHCIIpan_outputs")
    os.makedirs(netmhciipan_outputs_dir, exist_ok=True)  # Create the folder if it doesn't exist

    # Locate the alleleList.txt file in the script folder
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    allele_file_path = os.path.join(script_dir, "alleleList.txt")
    if not os.path.isfile(allele_file_path):
        raise FileNotFoundError(f"No file named 'alleleList.txt' found in the script folder: {script_dir}")

    # Read alleles from alleleList.txt
    with open(allele_file_path, "r") as allele_file:
        alleles = [line.strip() for line in allele_file if line.strip()]  # Strip whitespace and ignore empty lines
    if not alleles:
        raise ValueError("No alleles found in 'alleleList.txt'. Please ensure the file contains valid allele entries.")
    alleles_str = ",".join(alleles)

    # Define the output file in the new directory
    output_file = os.path.join(netmhciipan_outputs_dir, "mutated_peptide_sequences.pep.out")
    output_xls_file = os.path.join(netmhciipan_outputs_dir, "NetMHCIIpan_out.xls")

    # Construct the NetMHCIIpan command
    command = f"{netmhciipan_executable} -inptype 1 -f {pep_file} > {output_file} -a {alleles_str} -xls -xlsfile {output_xls_file}"

    # Print and execute the command
    print(f"Executing NetMHCIIpan command:\n{command}")
    subprocess.run(command, shell=True, check=True)

    print(f"NetMHCIIpan prediction completed. Output saved to: {output_file}")
