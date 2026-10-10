import pandas as pd
import numpy as np

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

p2rank_result = pd.read_csv('/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Homeworks/Homework_4/p2rank_2.5/test_output/predict_ACVR1_WT/ACVR1_WT.pdb_predictions.csv')
training_dataset = pd.read_csv("training_file_V2.csv")

training_dataset["Pocket_ID"] = training_dataset["Pocket_ID"].apply(lambda x: "pocket"+str(int(x.replace("pocket", ""))+1))

for feature in ["pocket_score", "pocket_probability", "pocket_sas_points", "pocket_surf_atoms", "variant_grantham_score"]:
    training_dataset[feature] = np.nan

for i in range(len(p2rank_result)):
    for j in range(len(training_dataset)):
        if p2rank_result["name     "][i] == str(training_dataset["Pocket_ID"][j]+"  "):
            training_dataset["pocket_score"][j] = p2rank_result["   score"][i]
            training_dataset["pocket_probability"][j] = p2rank_result[" probability"][i]
            training_dataset["pocket_sas_points"][j] = p2rank_result[" sas_points"][i]
            training_dataset["pocket_surf_atoms"][j] = p2rank_result[" surf_atoms"][i]

for i in range(len(training_dataset)):
    Variant = training_dataset["Variant"][i].split("_")[1]
    WT = Variant[0]
    Mut = Variant[-1]
    training_dataset["variant_grantham_score"][i] = getGranthamScore(WT, Mut)
training_dataset.to_csv("test_Grantham.csv", index=False)
print(training_dataset)

