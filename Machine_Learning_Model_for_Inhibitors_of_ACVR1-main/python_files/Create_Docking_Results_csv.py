import pandas as pd
import os
import regex as re
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import QED

ACVR1_variants = ["ACVR1_G325A", "ACVR1_G328E", "ACVR1_G328R", "ACVR1_G328W", "ACVR1_G356D", "ACVR1_L196P", "ACVR1_Q207E", "ACVR1_R202I", "ACVR1_R206H", "ACVR1_R258G", "ACVR1_R258S", "ACVR1_R375P", "ACVR1_WT"]

directory = '/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/failed_runs_results'

results_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith("config_log.txt")]

df_columns = ["Variant", "Inhibitor_ID", "Pocket_ID", "SMILES", "Binding_Affinity", "IC50", "MW", "LogP", "TPSA", "HBA", "HBD", "RotBonds", "Lipinski_Pass", "QED_Score"]

SMILES_file = "/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/SMILES/Inhibitor_SMILES.smi"

def getIC50(binding_affinity, temp=298.15):
    R = 1.987e-3
    Kd = np.exp(float(binding_affinity) / (temp*R))
    IC50 = Kd * 1e9
    return round(IC50, 2)

def getDescriptors(SMILES):
    mol = Chem.MolFromSmiles(SMILES)
    if mol is None:
        return None

    lipinski_violations = 0
    mw = Descriptors.MolWt(mol)
    tpsa = Descriptors.TPSA(mol)
    logp = Descriptors.MolLogP(mol)
    hba = Descriptors.NumHAcceptors(mol)
    hbd = Descriptors.NumHDonors(mol)
    RotBonds = Descriptors.NumRotatableBonds(mol)

    if mw > 500:
        lipinski_violations += 1
    if logp > 5:
        lipinski_violations += 1
    if hba > 10:
        lipinski_violations += 1
    if hbd > 5:
        lipinski_violations += 1
    QED_score = QED.qed(mol)
    return mw, logp, tpsa, hba, hbd, RotBonds, lipinski_violations, QED_score

results_df = pd.DataFrame(columns = df_columns)
print(results_df)
no_results = []
inhibitor_n_smiles = {}
for file in results_files:
    print(file)
    if ",variant" in file:
        new_name = re.sub(",variant", "", file)
        os.rename(file, new_name)
        file = new_name
        print(file)
    with open(file, "r") as result_file:
        content = str(result_file.read())
        match = re.search(r"\-\d+\.\d+", content)
        if not match:
            no_results.append(file)
            continue
        binding_affinity = match.group(0)
        print(binding_affinity)
        IC50 = getIC50(binding_affinity)
        print(IC50)
    for variant in ACVR1_variants:
        if variant in file:
            variant_name = variant
            print(variant_name)
            inhibitor_name_match = re.search(variant+"([0-9A-Z]+\_?[0-9A-Z]+)+pocket", file)
            inhibitor_name = inhibitor_name_match.group(1)
            print(inhibitor_name)
            pocket_match = re.search("(pocket\d)config", file)
            pocket = pocket_match.group(1)
            print(pocket)
            if inhibitor_name.startswith("CHEMBL"):
                with open(SMILES_file, "r") as SMILES:
                    content = SMILES.read()
                    if re.search(r"([A-Za-z\#\-\[\]\=\+\\\/\@\(\)0-9]+)\t"+inhibitor_name, content):
                        match = re.search(r"([A-Za-z\#\-\[\]\=\+\\\/\@\(\)0-9]+)\t"+inhibitor_name, content)
                        smiles = match.group(1)
                        MW, LogP, TPSA, HBA, HBD, RotBonds, lipinski_violations,QED_score = getDescriptors(smiles)
                        print(MW)
                        print(LogP)
                        print(TPSA)
                        print(HBA)
                        print(HBD)
                        print(RotBonds)
                        print(lipinski_violations)
                        print(QED_score)
            else:
                inhibitor_ID = inhibitor_name.split("_")[1]
                print(inhibitor_ID)
                if inhibitor_ID not in inhibitor_n_smiles:
                    url = 'https://www.rcsb.org/ligand/'+inhibitor_ID
                    driver = webdriver.Safari()
                    driver.get(url)
                    wait = WebDriverWait(driver, 10)
                    td_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.breakWord")))
                    smiles = next((td.text for td in td_elements if "C" in td.text), None)
                    inhibitor_n_smiles[inhibitor_ID] = smiles
                    print(inhibitor_n_smiles)
                    driver.quit()
                MW, LogP, TPSA, HBA, HBD, RotBonds, lipinski_violations, QED_score = getDescriptors(inhibitor_n_smiles[inhibitor_ID])
                print(MW)
                print(LogP)
                print(TPSA)
                print(HBA)
                print(HBD)
                print(RotBonds)
                print(lipinski_violations)
                print(QED_score)





    values = {"Variant": variant_name, "Inhibitor_ID": inhibitor_name, "Pocket_ID": pocket, "SMILES": smiles, "Binding_Affinity": binding_affinity, "IC50": IC50, "MW":MW, "LogP":LogP, "TPSA":TPSA, "HBA":HBA, "HBD":HBD, "RotBonds":RotBonds, "Lipinski_Pass":lipinski_violations, "QED_Score":QED_score}
    results_df.loc[len(results_df)] = values
results_df.to_csv("training_file_failed_runs.csv", index=False)
print(no_results)