import os

def save_mutated_peptides_to_pep(mutation_df, output_dir):
    """
    Save all mutated peptides to a .pep file.

    Parameters:
        mutation_df (DataFrame): DataFrame containing mutation data.
        output_dir (str): Path to the output directory.

    Output:
        Saves a file named 'mutated_peptide_sequences.pep' in the output directory.
    """
    # Extract all mutated peptides from the DataFrame
    mutated_peptides = []
    for peptides in mutation_df['mutate_peptide_list']:
        if peptides:  # Ensure the list is not None or empty
            mutated_peptides.extend(peptides)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the peptides to a .pep file
    output_file_path = os.path.join(output_dir, "mutated_peptide_sequences.pep")
    with open(output_file_path, 'w') as f:
        for peptide in mutated_peptides:
            f.write(f"{peptide}\n")

    print(f"Mutated peptide sequences have been saved to: {output_file_path}")
