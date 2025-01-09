from vcf_path_prompt import vcf_path_prompt
from annovar_dir_search import find_or_prompt_annovar_path
from trigger_annovar import trigger_annovar
from fasta_to_df import fasta_to_dataframe
from drop_imme_stopgain import filter_immediate_stopgain

vcf_file_path = vcf_path_prompt()
if vcf_file_path:
    print("Looking for ANNOVAR directory......")

annovar_path = find_or_prompt_annovar_path()
print(f"Your ANNOVAR path is set to: {annovar_path}")

fasta_path = trigger_annovar(vcf_file_path=vcf_file_path, annovar_path=annovar_path)
print("The fasta file is at: ", fasta_path, "     Start converting to DataFrame.......")

df = fasta_to_dataframe(fasta_path)
print("Filtering out immediate-stopgain.........")
filtered_df = filter_immediate_stopgain(df)
print("Filtering done!")
print(filtered_df.head())