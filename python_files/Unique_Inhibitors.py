import os

only_inhibitors = '/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/Only_Inhibitors'

unique_ids = set()

for filename in os.listdir(only_inhibitors):
    PDB_n_Ligand = filename.split("_")
    if len(PDB_n_Ligand) == 2:
        if PDB_n_Ligand[1] not in unique_ids:
            unique_ids.add(PDB_n_Ligand[1])
            filepath = os.path.join(only_inhibitors, filename)
            output_folder = '/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/Unique_Ligands'
            output_path = os.path.join(output_folder, filename)
            os.rename(filepath, output_path)