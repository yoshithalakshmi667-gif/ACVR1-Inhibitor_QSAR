import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt

training_dataset = pd.read_csv("/Users/victor_torres/PycharmProjects/AnalysisModelingBioStruc/test_Grantham.csv")

training_dataset.dropna(subset=["IC50", "MW", "LogP", "TPSA", "HBA", "HBD", "RotBonds", "Lipinski_Pass", "QED_Score", "pocket_score", "pocket_probability", "pocket_sas_points", "pocket_surf_atoms", "variant_grantham_score"], inplace=True)
training_dataset["Log_IC50"] = np.log10(training_dataset["IC50"])
training_dataset = pd.get_dummies(training_dataset, columns=["Variant", "Pocket_ID"])
unique_inhibitors = training_dataset["Inhibitor_ID"].unique()
train_ids, test_ids = train_test_split(unique_inhibitors, test_size=0.2, random_state=42)

train_data = training_dataset[training_dataset["Inhibitor_ID"].isin(train_ids)]
test_data = training_dataset[training_dataset["Inhibitor_ID"].isin(test_ids)]

X_train = train_data.drop(columns=["IC50", "SMILES", "Inhibitor_ID", "Log_IC50"])
Y_train = train_data["Log_IC50"]
X_test = test_data.drop(columns=["IC50", "SMILES", "Inhibitor_ID", "Log_IC50"])
Y_test = test_data["Log_IC50"]
rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train, Y_train)

Y_pred = rf.predict(X_test)

rmse = sqrt(mean_squared_error(Y_test, Y_pred,))
r2 = r2_score(Y_test, Y_pred)

print(f"RMSE (log IC50): {rmse:.3f}")
print(f"R² score: {r2:.3f}")
