import os
import pandas as pd
from netMHCIIpan_related.cluster_result import cluster_peptides_by_gene

def process_MixMHC2pred_results(input_file, output_dir, mutated_peptides_df_with_genes, gene_expression_file, tpm_threshold):
    """
    Process MixMHC2pred results, integrate gene expression data, perform clustering, and save each allele's data.

    Parameters:
    - input_file: Path to the input MixMHC2pred results file.
    - output_dir: Directory to save individual allele CSV files.
    - mutated_peptides_df_with_genes: DataFrame containing peptides and corresponding genes.
    - gene_expression_file: Path to the gene expression data CSV.
    - tpm_threshold: User-defined threshold for filtering based on gene expression.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Read MixMHC2pred output, skipping first 19 lines (metadata)
    df = pd.read_csv(input_file, sep="\t", skiprows=19)

    # Step 2: Extract allele-specific columns (%Rank_allele), ignoring %Rank_best
    allele_cols = [col for col in df.columns if col.startswith("%Rank_") and col != "%Rank_best"]

    # Step 3: Read gene expression data
    gene_expression_df = pd.read_csv(gene_expression_file)
    gene_expression_df.drop_duplicates(subset=["gene_name"], keep="first", inplace=True)
    gene_expression_df.set_index("gene_name", inplace=True)

    # Step 4: Map peptides to gene names
    peptide_to_gene = {}
    for _, row in mutated_peptides_df_with_genes.iterrows():
        if isinstance(row["mutate_peptide_list"], list):
            for peptide in row["mutate_peptide_list"]:
                peptide_to_gene[peptide] = row["Gene Name"]

    # Step 5: Process each allele and save results
    for allele_col in allele_cols:
        allele_name = allele_col.replace("%Rank_", "")  # Extract allele name
        filtered = df[df[allele_col] <= 5].copy()  # Filter rows where allele-specific rank ≤ 5

        # Add gene names based on peptide sequence
        filtered["Gene Name"] = filtered["Peptide"].map(peptide_to_gene).fillna("Unknown")

        # Remove rows where Gene Name is "Unknown"
        filtered = filtered[filtered["Gene Name"] != "Unknown"]

        # Add gene expression values
        filtered["Gene Expression"] = filtered["Gene Name"].map(gene_expression_df["tpm_sampleTest"])

        # Remove rows where Gene Expression is NA or 0
        filtered.dropna(subset=["Gene Expression"], inplace=True)
        filtered = filtered[filtered["Gene Expression"] > 0]

        # Add a binary column to indicate whether it meets the TPM threshold
        filtered["Considered Target"] = (filtered["Gene Expression"] >= tpm_threshold).astype(int)

        # Step 6: Perform peptide clustering by gene
        clustered_data = cluster_peptides_by_gene(filtered[["Gene Name", "Peptide"]])

        # Merge clustering results back to the filtered DataFrame
        filtered = filtered.merge(clustered_data, on=["Gene Name", "Peptide"], how="left")

        # ---- Merge extra information from mutated_peptides_df_with_genes ----
        extra_cols = ["Transcript ID", "cDNA Change", "Protein Change", "Mutation Type", "Description"]
        filtered = filtered.merge(
            mutated_peptides_df_with_genes[["Gene Name"] + extra_cols].drop_duplicates(),
            on="Gene Name", how="left"
        )

        # Remove wildtype rows
        filtered = filtered[filtered["Mutation Type"] != "WILDTYPE"]

        # Select relevant columns for output
        selected_columns = ["Peptide", "Gene Name", "Gene Expression", "Considered Target", "Cluster"] + extra_cols + [allele_col]
        filtered = filtered[selected_columns]

        # Rename columns for clarity
        filtered.rename(columns={allele_col: "Rank"}, inplace=True)

        # Sort by Rank (ascending order)
        filtered = filtered.sort_values(by="Rank")

        # Define output file path
        output_file = os.path.join(output_dir, f"{allele_name}_results.csv")

        # Save the filtered results to CSV
        filtered.to_csv(output_file, index=False)
        print(f"Results for allele {allele_name} saved to: {output_file}")
