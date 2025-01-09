import subprocess
import os


def trigger_annovar(vcf_file_path, annovar_path):
    """
    Function to process VCF files with ANNOVER in Linux.
    """

    ### Ensure the 'all_outputs' folder exists ###
    base_dir = os.path.dirname(annovar_path)  # Get the parent directory of the annovar path
    output_dir = os.path.join(base_dir, "all_outputs")
    os.makedirs(output_dir, exist_ok=True)  # Create the folder if it doesn't exist

    ### 1) Convert .vcf to .avinput ###
    if not vcf_file_path.endswith('.vcf'):
        raise ValueError("Your input file is not .vcf")

    filename = os.path.splitext(os.path.basename(vcf_file_path))[0]  # Get the filename without extension
    avinput_file = os.path.join(output_dir, f"{filename}.avinput")  # Save avinput in the output folder

    # Correctly reference the `convert2annovar.pl` script
    convert2annovar = os.path.join(annovar_path, 'convert2annovar.pl')

    # Construct the command for subprocess
    first_command = f"perl {convert2annovar} -format vcf4 {vcf_file_path} > {avinput_file}"

    # Print and execute the command
    print(f"1st code: {first_command}")
    subprocess.run(first_command, shell=True, check=True)

    ### 2) Annotate the variant file ###
    table_annovar = os.path.join(annovar_path, 'table_annovar.pl')
    humandb = os.path.join(annovar_path, 'humandb/')
    annotation_output_prefix = os.path.join(output_dir, filename)  # Output files from this step go to output_dir
    second_code = f"perl {table_annovar} {avinput_file} {humandb} -buildver hg19 -out {annotation_output_prefix} -protocol refGene -operation g -polish"

    print(f"2nd code: {second_code}")
    subprocess.run(second_code, shell=True, check=True)

    ### 3) Get Fasta File ###
    coding_change = os.path.join(annovar_path, 'coding_change.pl')
    exonic_variant_function = os.path.join(output_dir, f"{filename}.refGene.exonic_variant_function")
    hg19_refGene_txt = os.path.join(annovar_path, 'humandb/hg19_refGene.txt')
    hg19_refGene_fa = os.path.join(annovar_path, 'humandb/hg19_refGeneMrna.fa')
    fasta_output = os.path.join(output_dir, f"{filename}.mutated_proteins.fasta")  # Save fasta in output_dir

    third_command = f"perl {coding_change} {exonic_variant_function} {hg19_refGene_txt} {hg19_refGene_fa} -includesnp -onlyAltering > {fasta_output}"
    print(f"3rd command: {third_command}")
    subprocess.run(third_command, shell=True, check=True)

    return fasta_output