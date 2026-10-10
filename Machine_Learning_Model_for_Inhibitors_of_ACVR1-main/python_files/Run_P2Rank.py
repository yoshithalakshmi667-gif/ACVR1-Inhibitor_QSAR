import subprocess
import os

PDB_files = [file for file in os.listdir() if file.endswith(".pdb")]

for file in PDB_files:
    command = ["./prank", "predict", "-f", file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)