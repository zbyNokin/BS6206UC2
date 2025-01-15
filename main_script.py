import os
from annovar_related.vcf_path_prompt import vcf_path_prompt
from annovar_related.annovar_dir_search import find_or_prompt_annovar_path
from annovar_related.trigger_annovar import trigger_annovar
from annovar_related.fasta_to_df import fasta_to_dataframe
from annovar_related.drop_imme_stopgain import filter_immediate_stopgain
from annovar_related.mut_pep_generator import mut_pep_generator
from annovar_related.extract_gene_name import extract_gene_names_from_dynamic_file
from annovar_related.pep_file_generator import save_mutated_peptides_to_pep
from netMHCIIpan_related.neMHCIIpan_postprocess import process_netMHCIIpan_results_by_allele

from netMHCIIpan_related.netMHCIIpan_path_prompt import find_or_prompt_netMHCIIpan_path
from netMHCIIpan_related.trigger_netMHCIIpan import trigger_netMHCIIpan

# Step 1: Prompt vcf file
vcf_file_path = vcf_path_prompt()
if vcf_file_path:
    print("Looking for ANNOVAR directory......")

# Step 2: Find or prompt ANNOVAR path
annovar_path = find_or_prompt_annovar_path()
base_dir = os.path.dirname(annovar_path)
annovar_output_dir = os.path.join(base_dir, "annovar_outputs")
print(f"Your ANNOVAR path is set to: {annovar_path}")

# Step 3: Run ANNOVAR
fasta_path = trigger_annovar(vcf_file_path=vcf_file_path, annovar_path=annovar_path)
print("The fasta file is at: ", fasta_path, "     Start converting to DataFrame.......")

# Step 4: Convert fasta to DataFrame
df = fasta_to_dataframe(fasta_path)

# Step 5: Filter out immediate-stopgain
print("Filtering out immediate-stopgain.........")
mutation_df = filter_immediate_stopgain(df)
print("Filtering done!")
# print(mutation_df.head())

# Step 6: Generate mutation peptide sequences
mutated_peptides_df = mut_pep_generator(mutation_df)
print("Mutation peptide sequences extracted!")
# print(mutated_peptides_df.head())

# Step 7: Bind with Gene name (for gene expression analysis)
mutated_peptides_df_with_genes = extract_gene_names_from_dynamic_file(
    vcf_file_path=vcf_file_path,
    output_dir=annovar_output_dir,
    mutated_peptides_df=mutated_peptides_df
)
print(mutated_peptides_df_with_genes.head())

# Step 8: Generate .pep file
save_mutated_peptides_to_pep(mutated_peptides_df_with_genes, annovar_output_dir)

#------------------------------------------------------------------
# Step 9: Find or prompt netMHCIIpan path
netMHCIIpan_path = find_or_prompt_netMHCIIpan_path()
print(f"Your netMHCIIpan path is set to: {netMHCIIpan_path}")

# Step 10: Run netMHCIIpan
# trigger_netMHCIIpan(netMHCIIpan_path, annovar_output_dir)
netMHCIIpan_output_dir = os.path.join(base_dir, "netMHCIIpan_outputs")

# Step 11: Post-process NetMHCIIpan results
netMHCIIpan_results_file = os.path.join(netMHCIIpan_output_dir, "NetMHCIIpan_out.txt")
allele_results_dir = os.path.join(netMHCIIpan_output_dir, "allele_results")
print("Processing NetMHCIIpan results by allele...")
process_netMHCIIpan_results_by_allele(netMHCIIpan_results_file, allele_results_dir)
print("Allele-specific results saved in:", allele_results_dir)
