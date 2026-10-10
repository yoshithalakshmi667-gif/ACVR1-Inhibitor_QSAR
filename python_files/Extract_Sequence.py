import os
import pymol

three_to_one = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"
}

PDB_Files = [PDB_file for PDB_file in os.listdir() if PDB_file.endswith(".pdb")]

with open(f"allsequences.fasta", "w") as new_fasta:
    for file in PDB_Files:
        pymol.cmd.reinitialize()
        pymol.cmd.load(file, "protein")

        sequence = ""
        unique_residues = set()

        for resi in pymol.cmd.get_model("polymer").atom:
            res_id = (resi.resi, resi.chain)
            if res_id not in unique_residues:
                unique_residues.add(res_id)
                resn = resi.resn
                one_letter = three_to_one.get(resn, "X")
                sequence += one_letter

        filename = file.split(".")[0]

        new_fasta.write(f">{filename}\n{sequence}")
