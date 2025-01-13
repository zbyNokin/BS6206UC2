import os
import pandas as pd


def extract_gene_names_from_dynamic_file(vcf_file_path, output_dir, mutated_peptides_df):
    """
    Extract gene names from dynamically generated exonic_variant_function file
    based on the VCF file name and map them to the mutated_peptides_df.

    Parameters:
        vcf_file_path (str): Path to the VCF file provided by the user.
        output_dir (str): Path to the directory where output files are stored.
        mutated_peptides_df (pd.DataFrame): DataFrame containing mutated peptide data.

    Returns:
        pd.DataFrame: Updated mutated_peptides_df with a new column for gene names.
    """
    # Extract the base name of the VCF file (e.g., 'bs6206' from 'bs6206.vcf')
    filename_base = os.path.splitext(os.path.basename(vcf_file_path))[0]
    variant_file_path = os.path.join(output_dir, f"{filename_base}.refGene.exonic_variant_function")

    if not os.path.exists(variant_file_path):
        raise FileNotFoundError(f"The file {variant_file_path} does not exist.")

    # Read the variant file
    with open(variant_file_path, 'r') as file:
        variant_lines = file.readlines()

    # Extract gene names for each line
    gene_mapping = {}
    for line in variant_lines:
        columns = line.strip().split('\t')
        if len(columns) >= 3:  # Ensure there are enough columns
            gene_info = columns[2]  # Get the third column
            gene_name = gene_info.split(':')[0]  # Extract the gene name
            # Add the variant line (e.g., 'line1') as key and gene name as value
            gene_mapping[columns[0]] = gene_name

    # Ensure 'Variant ID' exists in mutated_peptides_df for mapping
    if 'Variant ID' in mutated_peptides_df.columns:
        mutated_peptides_df['Gene Name'] = mutated_peptides_df['Variant ID'].map(gene_mapping)
    else:
        print("Column 'Variant ID' is not in mutated_peptides_df!")

    return mutated_peptides_df
