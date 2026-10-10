import subprocess
import os

smiFiles = [smi_file for smi_file in os.listdir() if smi_file.endswith(".smi")]
for file in smiFiles:
    with open(file, "r") as SMILES_File:
        for line in SMILES_File:
            SMILE = str(line).split("\t")
            SMILE[1] = SMILE[1].replace("\n", "")

            command = ["obabel", "-:"+ SMILE[0], "-o", "pdb", "-O", SMILE[1]+".pdb", "--gen3d"]
            print(command)
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

