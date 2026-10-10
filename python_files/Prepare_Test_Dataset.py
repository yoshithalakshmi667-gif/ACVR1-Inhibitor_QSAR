from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import QED
import numpy as np
import regex as re
import time

grantham_scores = {
    ('A', 'C'): 195, ('A', 'D'): 126, ('A', 'E'): 107, ('A', 'F'): 113, ('A', 'G'): 60,
    ('A', 'H'): 86,  ('A', 'I'): 94,  ('A', 'K'): 106, ('A', 'L'): 96,  ('A', 'M'): 84,
    ('A', 'N'): 111, ('A', 'P'): 27,  ('A', 'Q'): 91,  ('A', 'R'): 112, ('A', 'S'): 99,
    ('A', 'T'): 58,  ('A', 'V'): 64,  ('A', 'W'): 148, ('A', 'Y'): 112,
    ('C', 'D'): 154, ('C', 'E'): 170, ('C', 'F'): 205, ('C', 'G'): 159, ('C', 'H'): 174,
    ('C', 'I'): 198, ('C', 'K'): 202, ('C', 'L'): 198, ('C', 'M'): 196, ('C', 'N'): 139,
    ('C', 'P'): 169, ('C', 'Q'): 154, ('C', 'R'): 180, ('C', 'S'): 112, ('C', 'T'): 149,
    ('C', 'V'): 192, ('C', 'W'): 215, ('C', 'Y'): 194,
    ('D', 'E'): 45,  ('D', 'F'): 177, ('D', 'G'): 94,  ('D', 'H'): 81,  ('D', 'I'): 168,
    ('D', 'K'): 101, ('D', 'L'): 172, ('D', 'M'): 160, ('D', 'N'): 23,  ('D', 'P'): 108,
    ('D', 'Q'): 61,  ('D', 'R'): 96,  ('D', 'S'): 65,  ('D', 'T'): 85,  ('D', 'V'): 152,
    ('D', 'W'): 181, ('D', 'Y'): 160,
    ('E', 'F'): 140, ('E', 'G'): 98,  ('E', 'H'): 40,  ('E', 'I'): 134, ('E', 'K'): 56,
    ('E', 'L'): 138, ('E', 'M'): 126, ('E', 'N'): 42,  ('E', 'P'): 93,  ('E', 'Q'): 29,
    ('E', 'R'): 54,  ('E', 'S'): 80,  ('E', 'T'): 65,  ('E', 'V'): 121, ('E', 'W'): 152,
    ('E', 'Y'): 122,
    ('F', 'G'): 153, ('F', 'H'): 100, ('F', 'I'): 21,  ('F', 'K'): 102, ('F', 'L'): 22,
    ('F', 'M'): 28,  ('F', 'N'): 158, ('F', 'P'): 114, ('F', 'Q'): 116, ('F', 'R'): 97,
    ('F', 'S'): 155, ('F', 'T'): 103, ('F', 'V'): 50,  ('F', 'W'): 40,  ('F', 'Y'): 22,
    ('G', 'H'): 98,  ('G', 'I'): 135, ('G', 'K'): 127, ('G', 'L'): 138, ('G', 'M'): 127,
    ('G', 'N'): 80,  ('G', 'P'): 42,  ('G', 'Q'): 87,  ('G', 'R'): 125, ('G', 'S'): 56,
    ('G', 'T'): 59,  ('G', 'V'): 109, ('G', 'W'): 184, ('G', 'Y'): 147,
    ('H', 'I'): 94,  ('H', 'K'): 32,  ('H', 'L'): 99,  ('H', 'M'): 87,  ('H', 'N'): 68,
    ('H', 'P'): 77,  ('H', 'Q'): 24,  ('H', 'R'): 29,  ('H', 'S'): 89,  ('H', 'T'): 47,
    ('H', 'V'): 84,  ('H', 'W'): 115, ('H', 'Y'): 83,
    ('I', 'K'): 102, ('I', 'L'): 5,   ('I', 'M'): 10,  ('I', 'N'): 149, ('I', 'P'): 95,
    ('I', 'Q'): 109, ('I', 'R'): 97,  ('I', 'S'): 142, ('I', 'T'): 89,  ('I', 'V'): 29,
    ('I', 'W'): 61,  ('I', 'Y'): 99,
    ('K', 'L'): 113, ('K', 'M'): 95,  ('K', 'N'): 94,  ('K', 'P'): 103, ('K', 'Q'): 53,
    ('K', 'R'): 26,  ('K', 'S'): 121, ('K', 'T'): 78,  ('K', 'V'): 97,  ('K', 'W'): 110,
    ('K', 'Y'): 85,
    ('L', 'M'): 15,  ('L', 'N'): 153, ('L', 'P'): 98,  ('L', 'Q'): 113, ('L', 'R'): 102,
    ('L', 'S'): 145, ('L', 'T'): 92,  ('L', 'V'): 32,  ('L', 'W'): 61,  ('L', 'Y'): 85,
    ('M', 'N'): 142, ('M', 'P'): 87,  ('M', 'Q'): 101, ('M', 'R'): 91,  ('M', 'S'): 135,
    ('M', 'T'): 81,  ('M', 'V'): 21,  ('M', 'W'): 67,  ('M', 'Y'): 77,
    ('N', 'P'): 91,  ('N', 'Q'): 46,  ('N', 'R'): 86,  ('N', 'S'): 46,  ('N', 'T'): 65,
    ('N', 'V'): 133, ('N', 'W'): 174, ('N', 'Y'): 143,
    ('P', 'Q'): 76,  ('P', 'R'): 103, ('P', 'S'): 74,  ('P', 'T'): 38,  ('P', 'V'): 68,
    ('P', 'W'): 147, ('P', 'Y'): 110,
    ('Q', 'R'): 43,  ('Q', 'S'): 68,  ('Q', 'T'): 42,  ('Q', 'V'): 96,  ('Q', 'W'): 130,
    ('Q', 'Y'): 99,
    ('R', 'S'): 110, ('R', 'T'): 71,  ('R', 'V'): 96,  ('R', 'W'): 101, ('R', 'Y'): 77,
    ('S', 'T'): 58,  ('S', 'V'): 124, ('S', 'W'): 177, ('S', 'Y'): 144,
    ('T', 'V'): 69,  ('T', 'W'): 128, ('T', 'Y'): 92,
    ('V', 'W'): 88,  ('V', 'Y'): 88,
    ('W', 'Y'): 37
}

def getGranthamScore(WildT, Mut):
    if WildT == Mut:
        return 0
    return grantham_scores.get((WildT, Mut)) or grantham_scores.get((Mut, WildT)) or np.nan

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


Inhibitors = []
SMILES_list = []
df_columns = ["Variant", "Inhibitor_ID", "Pocket_ID", "SMILES", "Binding_Affinity", "IC50", "MW", "LogP", "TPSA", "HBA", "HBD", "RotBonds", "Lipinski_Pass", "QED_Score", 'pocket_score', 'pocket_probability', 'pocket_sas_points', 'pocket_surf_atoms', 'variant_grantham_score']
ACVR1_variants = ["ACVR1_G325A", "ACVR1_G328E", "ACVR1_G328R", "ACVR1_G328W", "ACVR1_G356D", "ACVR1_L196P", "ACVR1_Q207E", "ACVR1_R202I", "ACVR1_R206H", "ACVR1_R258G", "ACVR1_R258S", "ACVR1_R375P", "ACVR1_WT"]
pockets = ["pocket1", "pocket2", "pocket3", "pocket4", "pocket5", "pocket6", "pocket7"]
input_file = pd.DataFrame(columns=df_columns)
for i in range(100):
    Website = "https://pubchem.ncbi.nlm.nih.gov/#query=Kinase%20Inhibitor&page="+str(i+1)
    driver = webdriver.Safari()
    driver.get(Website)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    name_blocks = soup.select('li.p-md-bottom span.breakword')

    inhibitor_names = []

    for block in name_blocks:
        name_text = block.get_text(strip=True)
        if name_text:
            inhibitor_names.append(name_text)

    driver.quit()

    #print("Compound Names Found:")
    matches = []
    #Inhibitors = []
    #SMILES_list = []
    for name in inhibitor_names:
        #print(name)
        matches.append(name)
        if re.match("^C\d+\s\-\s", matches[-1]):
            #print(matches)
            Inhibitors.append(matches[0].split(";")[0])
            SMILES_list.append(matches[5])
            print(Inhibitors)
            print(SMILES_list)
            print(len(Inhibitors))
            print(len(SMILES_list))
            matches = []
    if len(Inhibitors) >= 100:
        break
rows = []
for variant in ACVR1_variants:
    Variant = variant.split("_")[1]
    WT = Variant[0]
    Mut = Variant[-1]
    variant_grantham_score = getGranthamScore(WT, Mut)
    for pocket in pockets:
        'pocket_score', 'pocket_probability', 'pocket_sas_points', 'pocket_surf_atoms'
        if pocket == "pocket1":
            pocket_score = 12.62
            pocket_probability = 0.657
            pocket_sas_points = 83
            pocket_surf_atoms = 47
        elif pocket == "pocket2":
            pocket_score = 4.66
            pocket_probability = 0.203
            pocket_sas_points = 55
            pocket_surf_atoms = 28
        elif pocket == "pocket3":
            pocket_score = 4.2
            pocket_probability = 0.171
            pocket_sas_points = 72
            pocket_surf_atoms = 31
        elif pocket == "pocket4":
            pocket_score = 3.16
            pocket_probability = 0.107
            pocket_sas_points = 36
            pocket_surf_atoms = 22
        elif pocket == "pocket5":
            pocket_score = 1.49
            pocket_probability = 0.021
            pocket_sas_points = 24
            pocket_surf_atoms = 17
        elif pocket == "pocket6":
            pocket_score = 1.41
            pocket_probability = 0.018
            pocket_sas_points = 21
            pocket_surf_atoms = 11
        elif pocket == "pocket7":
            pocket_score = 1.33
            pocket_probability = 0.015
            pocket_sas_points = 7
            pocket_surf_atoms = 8
        for inhibitor, smiles in zip(Inhibitors, SMILES_list):
            MW, LogP, TPSA, HBA, HBD, RotBonds, lipinski_violations, QED_score = getDescriptors(smiles)
            rows.append({
                "Variant": variant,
                "Inhibitor_ID": inhibitor,
                "Pocket_ID": pocket,
                "SMILES": smiles,
                "MW": MW,
                "LogP": LogP,
                "TPSA": TPSA,
                "HBA": HBA,
                "HBD": HBD,
                "RotBonds": RotBonds,
                "Lipinski_Pass": lipinski_violations,
                "QED_score": QED_score,
                "pocket_score": pocket_score,
                "pocket_probability": pocket_probability,
                "pocket_sas_points": pocket_sas_points,
                "pocket_surf_atoms": pocket_surf_atoms,
                "variant_grantham_score": variant_grantham_score
            })

input_file = pd.DataFrame(rows)

input_file.to_csv("TEST_INHBITORS.csv", index=False)
print(Inhibitors)
print(SMILES_list)