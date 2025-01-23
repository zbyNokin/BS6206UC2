import os
import pandas as pd

def process_netMHCIIpan_results_by_allele(input_file, output_dir, mutated_peptides_df_with_genes, gene_expression_file):
    """
    Process NetMHCIIpan results, integrate gene expression data, and save each allele's data.

    Parameters:
    - input_file: Path to the input NetMHCIIpan results file.
    - output_dir: Directory to save individual allele CSV files.
    - mutated_peptides_df_with_genes: DataFrame containing peptides and corresponding genes.
    - gene_expression_file: Path to the gene expression data CSV.
    """
    # Step 1: Read the first two rows separately
    with open(input_file, "r") as f:
        first_line = f.readline().strip().split("\t")  # First line: Allele names
        second_line = f.readline().strip().split("\t")  # Second line: Column headers

    # Step 2: Ensure column names are unique
    seen = {}
    unique_second_line = []
    for col in second_line:
        if col not in seen:
            seen[col] = 0
            unique_second_line.append(col)
        else:
            seen[col] += 1
            unique_second_line.append(f"{col}_{seen[col]}")

    # Step 3: Create a mapping of allele to its column groups
    common_cols = ["Pos", "Peptide", "ID", "Target"]  # Shared columns
    allele_mapping = {}
    allele_start_idx = len(common_cols)

    for idx, name in enumerate(first_line):
        if name:  # Ignore empty names caused by extra tabs
            allele_mapping[name] = unique_second_line[allele_start_idx:allele_start_idx + 4]
            allele_start_idx += 4

    # Step 4: Read the actual data (skipping the first two rows)
    df = pd.read_csv(input_file, sep="\t", skiprows=2, names=unique_second_line)

    # Step 5: Remove duplicate gene entries in gene expression data and set index
    gene_expression_df = pd.read_csv(gene_expression_file)
    gene_expression_df.drop_duplicates(subset=["gene_name"], keep="first", inplace=True)
    gene_expression_df.set_index("gene_name", inplace=True)

    # Remove rows where TPM is 0 before calculating the median
    non_zero_gene_expression = gene_expression_df[gene_expression_df["tpm_sampleTest"] > 0]

    # Calculate and display median TPM value (excluding zeros)
    median_tpm = non_zero_gene_expression["tpm_sampleTest"].median()
    print(f"The median TPM value of the gene expression data (excluding zeros) is: {median_tpm:.2f}")

    # Step 6: Prompt user for TPM threshold
    while True:
        try:
            tpm_threshold = float(input(f"Please enter the TPM threshold (recommendation: > {median_tpm:.2f}): "))
            if tpm_threshold < 0:
                print("Threshold must be a non-negative number. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    # Step 7: Map peptides to gene names
    peptide_to_gene = {}
    for _, row in mutated_peptides_df_with_genes.iterrows():
        if isinstance(row["mutate_peptide_list"], list):
            for peptide in row["mutate_peptide_list"]:
                peptide_to_gene[peptide] = row["Gene Name"]

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 8: Process each allele and save results
    for allele, cols in allele_mapping.items():
        rank_col = cols[-1]  # Last column in the group is the 'Rank' column
        filtered = df[df[rank_col] <= 5].copy()  # Filter rows with Rank <= 5
        filtered = filtered.sort_values(by=rank_col)  # Sort by Rank ascending

        # Add gene names based on peptide sequence
        filtered["Gene Name"] = filtered["Peptide"].map(peptide_to_gene).fillna("Unknown")

        # Remove rows where Gene Name is "Unknown"
        filtered = filtered[filtered["Gene Name"] != "Unknown"]

        # Add gene expression values based on mapped gene name
        filtered["Gene Expression"] = filtered["Gene Name"].map(gene_expression_df["tpm_sampleTest"])

        # Remove rows where Gene Expression is NA or 0
        filtered.dropna(subset=["Gene Expression"], inplace=True)
        filtered = filtered[filtered["Gene Expression"] > 0]

        # Add a new binary column to indicate whether it meets the TPM threshold
        filtered["Considered Target"] = (filtered["Gene Expression"] >= tpm_threshold).astype(int)

        # Keep only relevant columns
        selected_columns = common_cols + ["Gene Name", "Gene Expression", "Considered Target"] + cols
        filtered = filtered[selected_columns]

        # Remove column suffixes (_0, _1, etc.) for output
        new_column_names = {col: col.split("_")[0] for col in filtered.columns}
        filtered.rename(columns=new_column_names, inplace=True)

        # Define the output file path
        output_file = os.path.join(output_dir, f"{allele}_results.csv")

        # Save the filtered results to CSV
        filtered.to_csv(output_file, index=False)
        print(f"Results for allele {allele} saved to: {output_file}")

