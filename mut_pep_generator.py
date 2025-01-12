import random

import pandas as pd
import re

def mut_pep_generator(input_df):
    insertion_count = 0
    deletion_count = 0
    frameshift_count = 0
    replacement_count = 0

    input_df = input_df.copy()
    input_df["mutate_peptide_list"] = None
    input_df["Protein Sequence"] = input_df["Protein Sequence"].str.rstrip('*')

    for index, row in input_df.iterrows():
        pep_list = []
        if row["Mutation Type"] == "protein-altering":
            # Insertion p.Q183_R184insQ
            if 'ins' in row['Protein Change']:
                insertion_count += 1

                mutation_info = row["Protein Change"].split('ins')
                position_range = mutation_info[0]  # Q183_R184
                inserted_sequence = mutation_info[1]  # AGDF

                pos = int(position_range.split('_')[0][3:])  # 183

                for peptide_length in range(12, 26):
                    for offset in range(peptide_length):
                        start = pos - peptide_length + offset
                        end = pos + offset
                        peptide = input_df.loc[index, "Protein Sequence"][start:end]

                        if (len(peptide) >= 12
                            and inserted_sequence in peptide # Check if all insertion part in seq
                            and peptide not in input_df.loc[index - 1, "Protein Sequence"] # Check duplication
                        ):
                            pep_list.append(peptide)
                input_df.at[index, "mutate_peptide_list"] = pd.Series(pep_list).unique().tolist()

            # Deletion p.E710del
            elif 'del' in row['Protein Change']:
                deletion_count += 1
                pos = int(row["Protein Change"].split('del')[0][3:]) - 1  # get index
                for peptide_length in range(12, 26):
                    for offset in range(peptide_length):
                        peptide = input_df.loc[index, "Protein Sequence"][pos - peptide_length + offset: pos + offset]
                        if len(peptide) >= 12 and peptide not in input_df.loc[index - 1, "Protein Sequence"]:
                            pep_list.append(peptide)
                input_df.at[index, "mutate_peptide_list"] = pd.Series(pep_list).unique().tolist()

            # Frameshift p.Y32Cfs*18
            elif 'fs' in row['Protein Change']:
                frameshift_count += 1
                pos = int(row["Protein Change"].split('fs')[0][3:-1]) - 1
                mut_length = int(row["Protein Change"].split('*')[1])
                for peptide_length in range(12, 26):
                    # Frameshift inner possible peptides
                    max_possible_peptides = mut_length - peptide_length + 1

                    if max_possible_peptides > 30:
                        # Random sample 30
                        sampled_positions = random.sample(
                            range(pos, pos + mut_length - peptide_length + 1), 30
                        )
                    else:
                        # Exhaustive Search
                        sampled_positions = range(pos, pos + mut_length - peptide_length + 1)

                    for start_pos in sampled_positions:
                        peptide = input_df.loc[index, "Protein Sequence"][start_pos:start_pos + peptide_length]
                        if len(peptide) >= 12 and peptide not in input_df.loc[index - 1, "Protein Sequence"]:
                            pep_list.append(peptide)
                input_df.at[index, "mutate_peptide_list"] = pd.Series(pep_list).unique().tolist()

            # Replacement p.G300D
            else:
                replacement_count += 1
                pos = int(row["Protein Change"].split('.')[1][1:-1]) - 1  # 获取替换的突变索引并修正
                for peptide_length in range(12, 26):
                    for offset in range(peptide_length):
                        peptide = input_df.loc[index, "Protein Sequence"][pos - peptide_length + offset: pos + offset]
                        if len(peptide) >= 12 and peptide not in input_df.loc[index - 1, "Protein Sequence"]:
                            pep_list.append(peptide)
                input_df.at[index, "mutate_peptide_list"] = pd.Series(pep_list).unique().tolist()

    print(f"Insertion Count: {insertion_count}")
    print(f"Deletion Count: {deletion_count}")
    print(f"Frameshift Count: {frameshift_count}")
    print(f"Replacement Count: {replacement_count}")

    return input_df


