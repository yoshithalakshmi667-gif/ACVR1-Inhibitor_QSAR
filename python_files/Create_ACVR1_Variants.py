import os
import pymol
import regex as re
import time

variants = ["L196P", "R202I", "Q207E", "R258S", "R258G", "G325A", "G328W", "G328E", "G328R", "G356D", "R375P"]
amino_acid_map = {
    "A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP", "C": "CYS",
    "E": "GLU", "Q": "GLN", "G": "GLY", "H": "HIS", "I": "ILE",
    "L": "LEU", "K": "LYS", "M": "MET", "F": "PHE", "P": "PRO",
    "S": "SER", "T": "THR", "W": "TRP", "Y": "TYR", "V": "VAL"
}

ACVR1_R206H = '/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/ACVR1_Variants/ACVR1_R206H,variant.pdb'

output_folder = '/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/ACVR1_Variants'

pymol.pymol_argv = ['pymol', '-c']
pymol.finish_launching()

pymol.cmd.load(ACVR1_R206H, "ACVR1_R206H")
pymol.cmd.create("ACVR1_WT", "ACVR1_R206H")
pymol.cmd.wizard('mutagenesis')
pymol.cmd.get_wizard().set_mode("ARG")
pymol.cmd.get_wizard().do_select('resi 206')
pymol.cmd.get_wizard().apply()
pymol.cmd.set_wizard()
pymol.cmd.alter("resi 206", "resn='ARG'")
pymol.cmd.rebuild()
wildtype_path = os.path.join(output_folder, "ACVR1_WT.pdb")
pymol.cmd.save(wildtype_path, "ACVR1_WT")

Wild_Type_Path = '/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/ACVR1_Variants/ACVR1_WT.pdb'
for variant in variants:
    #pymol.pymol_argv = ['pymol', '-c']
    #pymol.finish_launching()
    #pymol.cmd.delete("ACVR1_"+variant)
    #pymol.cmd.delete("ACVR1_WT")
    #pymol.cmd.create("ACVR1_WT", "ACVR1_R206H")
    pymol.cmd.reinitialize()
    pymol.cmd.load(Wild_Type_Path, "ACVR1_WT")
    pymol.cmd.create("ACVR1_" + variant, "ACVR1_WT")
    match = re.search(r"[A-Z]([0-9]+)[A-Z]", variant)
    position = match.group(1)
    mutation_aminoacid = variant[-1]
    pymol.cmd.wizard("mutagenesis")
    pymol.cmd.get_wizard().set_mode(amino_acid_map[mutation_aminoacid])
    pymol.cmd.get_wizard().do_select(f'resi {position}')
    pymol.cmd.get_wizard().apply()
    pymol.cmd.set_wizard()
    pymol.cmd.alter(f"resi {position}", f"resn='{amino_acid_map[mutation_aminoacid]}'")
    pymol.cmd.rebuild()
    pymol.cmd.refresh()
    variation_path = os.path.join(output_folder, f"ACVR1_{variant}.pdb")
    pymol.cmd.save(variation_path, f"ACVR1_{variant}")
pymol.cmd.quit()




