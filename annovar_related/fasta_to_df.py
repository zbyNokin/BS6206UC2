import pandas as pd

def fasta_to_dataframe(fasta_file):
    data = []
    identifier = ""
    sequence = []

    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            line = line.strip()
            if line.startswith(">"):
                if "WILDTYPE" not in line:
                    if identifier:
                        data.append(identifier + [''.join(sequence)])
                    identifier = line[1:].split(maxsplit=5)
                    sequence = []
                elif "WILDTYPE" in line:
                    if identifier:
                        data.append(identifier + [''.join(sequence)])
                    identifier = line[1:].split()
                    empty = "NA"
                    identifier = [identifier[0], identifier[1], empty, empty, identifier[2], empty]
                    sequence = []
            else:
                sequence.append(line)

        if identifier:
            data.append(identifier + [''.join(sequence)])

    df = pd.DataFrame(data, columns=["Variant ID", "Transcript ID", "cDNA Change",
                                     "Protein Change", "Mutation Type", "Description",
                                     "Protein Sequence"])
    return df