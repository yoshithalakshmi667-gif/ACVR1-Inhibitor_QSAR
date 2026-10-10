import os
import subprocess

PDB_Files = [file for file in os.listdir() if file.endswith(".pdb")]

for file in PDB_Files:
    CHEM_IDS = str(file).split(".")
    command = ["obabel", file, "-O", CHEM_IDS[0]+".pdbqt"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)