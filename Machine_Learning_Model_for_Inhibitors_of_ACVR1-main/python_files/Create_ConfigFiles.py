import os
import pandas as pd
#import subprocess

ACVR1_variants = [ACVR1 for ACVR1 in os.listdir() if ACVR1.startswith("ACVR1_") and ACVR1.endswith(".pdbqt")]

Inhibitors = [Ligand for Ligand in os.listdir() if not Ligand.startswith("ACVR1_") and Ligand.endswith(".pdbqt")]

pockets_df = pd.read_csv("ACVR1_WT.pdb_predictions.csv")

config_files = []
content = ""
for i in range(len(ACVR1_variants)):
    variant_name = ACVR1_variants[i].split(".")
    for j in range(len(Inhibitors)):
        inhibitor_name = Inhibitors[j].split(".")
        for w in range(len(pockets_df)):
            with open(variant_name[0]+inhibitor_name[0]+"pocket"+str(w)+"config.txt", "w") as config_file:
                config_files.append(variant_name[0]+inhibitor_name[0]+"pocket"+str(w)+"config.txt")
                content = "receptor = " + ACVR1_variants[i] + "\nligand = " + Inhibitors[j] + "\n\ncenter_x = " + str(float(pockets_df["   center_x"].iloc[w])) + "\ncenter_y = " + str(float(pockets_df["   center_y"].iloc[w])) + "\ncenter_z = " + str(float(pockets_df["   center_z"].iloc[w])) + "\n\nsize_x = 25\nsize_y = 25\nsize_z = 25\n\nenergy_range = 4"
                print(content)
                config_file.write(content)
        '''for z in range(len(config_files)):
            if inhibitor_name[0] in config_files[z]:
                command = ["vina", "--config", config_files[z], "--ligand", Inhibitors[j], "--out", variant_name[0] + inhibitor_name[0] + ".pdbqt", "--log", variant_name[0] + inhibitor_name[0] + "_log.txt"]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)'''