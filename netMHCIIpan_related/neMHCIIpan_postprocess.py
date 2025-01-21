import os
import pandas as pd

def process_netMHCIIpan_results_by_allele(input_file, output_dir, mutated_peptides_df_with_genes):
    """
    Process NetMHCIIpan results and save each allele's data with gene names to a separate CSV file.

    Parameters:
    - input_file: Path to the input NetMHCIIpan results file.
    - output_dir: Directory to save individual allele CSV files.
    - mutated_peptides_df_with_genes: DataFrame containing peptides and corresponding gene names.
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

    # Step 4: Read the actual data (skipping the first two rows as header)
    df = pd.read_csv(input_file, sep="\t", skiprows=2, names=unique_second_line)

    # Step 5: Create a peptide-to-gene mapping
    peptide_to_gene = {}
    for _, row in mutated_peptides_df_with_genes.iterrows():
        if row["mutate_peptide_list"] is not None and isinstance(row["mutate_peptide_list"], list):
            for peptide in row["mutate_peptide_list"]:
                peptide_to_gene[peptide] = row["Gene Name"]

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 6: Process each allele and save to separate CSV files
    for allele, cols in allele_mapping.items():
        rank_col = cols[-1]  # Last column in the group is the 'Rank' column
        filtered = df[df[rank_col] <= 5].copy()  # Filter rows with Rank <= 5
        filtered = filtered.sort_values(by=rank_col)  # Sort by Rank ascending

        # Add gene names based on peptide sequence
        filtered["Gene Name"] = filtered["Peptide"].map(peptide_to_gene).fillna("Unknown")

        # Only keep the allele's specific columns and the common columns
        selected_columns = common_cols + ["Gene Name"] + cols
        filtered = filtered[selected_columns]

        # Remove column suffixes (_0, _1, etc.) for output
        new_column_names = {col: col.split("_")[0] for col in filtered.columns}
        filtered.rename(columns=new_column_names, inplace=True)

        # Define the output file path
        output_file = os.path.join(output_dir, f"{allele}_results.csv")

        # Save to CSV
        filtered.to_csv(output_file, index=False)
        print(f"Results for allele {allele} saved to: {output_file}")
