import os
import subprocess

ACVR1_variants = [ACVR1 for ACVR1 in os.listdir() if ACVR1.startswith("ACVR1_") and ACVR1.endswith(".pdbqt")]

Inhibitors = [Ligand for Ligand in os.listdir() if not Ligand.startswith("ACVR1_") and Ligand.endswith(".pdbqt")]

Config_files = [txt_file for txt_file in os.listdir() if txt_file.endswith(".txt")]

for i in range(len(Inhibitors)):
    inhibitor_name = Inhibitors[i].split(".")
    for j in range(len(Config_files)):
        file_name = Config_files[j].split(".")
        if inhibitor_name[0] in Config_files[j]:
            command = ["vina", "--config", Config_files[j], "--ligand", Inhibitors[i], "--out",
                       file_name[0] + ".pdbqt", "--log",
                       file_name[0] + "_log.txt"]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
