import os
import pandas as pd
from annovar_related.vcf_path_prompt import vcf_path_prompt
from annovar_related.annovar_dir_search import find_or_prompt_annovar_path
from annovar_related.trigger_annovar import trigger_annovar
from annovar_related.fasta_to_df import fasta_to_dataframe
from annovar_related.drop_imme_stopgain import filter_immediate_stopgain
from annovar_related.mut_pep_generator import mut_pep_generator
from annovar_related.extract_gene_name import extract_gene_names_from_dynamic_file
from annovar_related.pep_file_generator import save_mutated_peptides_to_pep

from netMHCIIpan_related.netMHCIIpan_path_prompt import find_or_prompt_netMHCIIpan_path
from netMHCIIpan_related.trigger_netMHCIIpan import trigger_netMHCIIpan
from netMHCIIpan_related.netMHCIIpan_postprocess import process_netMHCIIpan_results_by_allele

from MixMHC2pred_related.mixMHC2pred_path_prompt import find_or_prompt_MixMHC2pred_path
from MixMHC2pred_related.trigger_mixMHC2pred import trigger_MixMHC2pred
from MixMHC2pred_related.mixMHC2pred_postprocess import process_MixMHC2pred_results

# ------------------- Step 1: Prompt for VCF File -------------------
vcf_file_path = vcf_path_prompt()
if vcf_file_path:
    print("Looking for ANNOVAR directory......")

# ------------------- Step 2: Find or Prompt ANNOVAR Path -------------------
annovar_path = find_or_prompt_annovar_path()
annovar_output_dir = os.path.join(os.path.dirname(annovar_path), "annovar_outputs")
print(f"Your ANNOVAR path is set to: {annovar_path}")

# ------------------- Step 3: Run ANNOVAR -------------------
fasta_path = trigger_annovar(vcf_file_path=vcf_file_path, annovar_path=annovar_path)
print("The fasta file is at: ", fasta_path, "     Start converting to DataFrame.......")

# ------------------- Step 4: Convert fasta to DataFrame -------------------
df = fasta_to_dataframe(fasta_path)

# ------------------- Step 5: Filter out immediate-stopgain -------------------
print("Filtering out immediate-stopgain.........")
mutation_df = filter_immediate_stopgain(df)
print("Filtering done!")

# ------------------- Step 6: Generate mutation peptide sequences -------------------
mutated_peptides_df = mut_pep_generator(mutation_df)
print("Mutation peptide sequences extracted!")

# ------------------- Step 7: Bind with Gene Name (for gene expression analysis) -------------------
mutated_peptides_df_with_genes = extract_gene_names_from_dynamic_file(
    vcf_file_path=vcf_file_path,
    output_dir=annovar_output_dir,
    mutated_peptides_df=mutated_peptides_df
)
print(mutated_peptides_df_with_genes.head())

# ------------------- Step 8: Generate .pep File -------------------
save_mutated_peptides_to_pep(mutated_peptides_df_with_genes, annovar_output_dir)

# ------------------- Step 9: Prompt for Gene Expression File -------------------
gene_expression_file = input("Enter the full path to the gene expression CSV file: ").strip()

# Read Gene Expression Data
gene_expression_df = pd.read_csv(gene_expression_file)
gene_expression_df.drop_duplicates(subset=["gene_name"], keep="first", inplace=True)
gene_expression_df.set_index("gene_name", inplace=True)

# Remove TPM = 0 before calculating the median
non_zero_gene_expression = gene_expression_df[gene_expression_df["tpm_sampleTest"] > 0]
median_tpm = non_zero_gene_expression["tpm_sampleTest"].median()
print(f"The median TPM value of the gene expression data (excluding zeros) is: {median_tpm:.2f}")

# Prompt for TPM Threshold
while True:
    try:
        tpm_threshold = float(input(f"Please enter the TPM threshold (recommendation: > {median_tpm:.2f}): "))
        if tpm_threshold < 0:
            print("Threshold must be a non-negative number. Please try again.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# ------------------- NetMHCIIpan Processing -------------------
# Step 10: Find or Prompt NetMHCIIpan Path
netMHCIIpan_path = find_or_prompt_netMHCIIpan_path()
print(f"Your NetMHCIIpan path is set to: {netMHCIIpan_path}")

# Step 11: Run NetMHCIIpan
trigger_netMHCIIpan(netMHCIIpan_path, annovar_output_dir)

# Step 12: Process NetMHCIIpan results
netMHCIIpan_output_file = os.path.join(os.path.dirname(annovar_output_dir), "netMHCIIpan_outputs", "NetMHCIIpan_out.txt")
netMHCIIpan_results_dir = os.path.join(os.path.dirname(annovar_output_dir), "netMHCIIpan_outputs", "allele_results")

process_netMHCIIpan_results_by_allele(netMHCIIpan_output_file, netMHCIIpan_results_dir, mutated_peptides_df_with_genes, gene_expression_file, tpm_threshold)

# ------------------- MixMHC2pred Processing -------------------
# Step 13: Find or Prompt MixMHC2pred Path
MixMHC2pred_path = find_or_prompt_MixMHC2pred_path()
print(f"Your MixMHC2pred path is set to: {MixMHC2pred_path}")

# Step 14: Run MixMHC2pred
trigger_MixMHC2pred(MixMHC2pred_path, annovar_output_dir)

# Step 15: Process MixMHC2pred results
MixMHC2pred_output_file = os.path.join(os.path.dirname(annovar_output_dir), "MixMHC2pred_outputs", "mutated_peptide_sequences_mix_out.txt")
MixMHC2pred_results_dir = os.path.join(os.path.dirname(annovar_output_dir), "MixMHC2pred_outputs", "allele_results")

process_MixMHC2pred_results(MixMHC2pred_output_file, MixMHC2pred_results_dir, mutated_peptides_df_with_genes, gene_expression_file, tpm_threshold)
