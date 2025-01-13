import os
from vcf_path_prompt import vcf_path_prompt
from annovar_dir_search import find_or_prompt_annovar_path
from trigger_annovar import trigger_annovar
from fasta_to_df import fasta_to_dataframe
from drop_imme_stopgain import filter_immediate_stopgain
from mut_pep_generator import mut_pep_generator
from extract_gene_name import extract_gene_names_from_dynamic_file

# Step 1: Prompt vcf file
vcf_file_path = vcf_path_prompt()
if vcf_file_path:
    print("Looking for ANNOVAR directory......")

# Step 2: Find or prompt ANNOVAR path
annovar_path = find_or_prompt_annovar_path()
output_dir = os.path.join(os.path.dirname(annovar_path), "all_outputs")
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
    output_dir=output_dir,
    mutated_peptides_df=mutated_peptides_df
)
print(mutated_peptides_df_with_genes.head())
