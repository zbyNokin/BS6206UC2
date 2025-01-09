from vcf_path_prompt import vcf_path_prompt
from annovar_dir_search import find_or_prompt_annovar_path

vcf_file_path = vcf_path_prompt()
if vcf_file_path:
    print("Looking for ANNOVAR directory......")

annovar_path = find_or_prompt_annovar_path()
print(f"Your ANNOVAR path is set to: {annovar_path}")