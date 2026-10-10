import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import ScalarFormatter

Results_CSV = pd.read_csv("/Users/victor_torres/PycharmProjects/AnalysisModelingBioStruc/training_file_V2.csv")
#print(Results_CSV)
columns = Results_CSV.columns
#print(columns)
variants = []
pockets = []

pocket_palette = {
    "pocket0": "#1f77b4",
    "pocket1": "#ff7f0e",
    "pocket2": "#2ca02c",
    "pocket3": "#d62728",
    "pocket4": "#9467bd",
    "pocket5": "#8c564b",
    "pocket6": "#e377c2",
}

for i in range(len(Results_CSV)):
    variants.append(Results_CSV.iloc[i]["Variant"])
    pockets.append(Results_CSV.iloc[i]["Pocket_ID"])
    unique_variants = list(set(variants))
    unique_pockets = list(set(pockets))
ordered_pockets = ["pocket"+str(i) for i in range(len(unique_pockets))]
for i in range(len(unique_variants)):
    new_df = pd.DataFrame(columns=columns)
    for j in range(len(Results_CSV)):
        #print(unique_variants[i])
        #print("_____")
        #print(Results_CSV.iloc[j]["Variant"])
        if Results_CSV.iloc[j]["Variant"] == unique_variants[i]:
            new_df.loc[len(new_df)] = Results_CSV.iloc[j]
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid")
    sns.lineplot(
        data=new_df,
        x="Inhibitor_ID",
        y="IC50",
        hue="Pocket_ID",
        hue_order=ordered_pockets,
        marker="o",
        markersize=2
    )
    plt.xticks(rotation=90, fontsize=4)
    plt.title(unique_variants[i])
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=False))
    ax.ticklabel_format(style='plain', axis='y')
    plt.savefig("IC50_Plot_"+unique_variants[i]+".png", dpi=300, bbox_inches='tight')
    g = sns.catplot(
        data=new_df,
        x="Variant",
        y="IC50",
        kind="box",
        hue="Pocket_ID",
        hue_order=ordered_pockets,
        height=6,
        aspect=2
    )
    plt.ylim(0, 80000)
    g.set_xticklabels(rotation=45)
    g.set_axis_labels("Variant", "IC50 (nM)")
    g.savefig("Boxplot_IC50_"+unique_variants[i]+"_and_Pocket.png", dpi=300, bbox_inches='tight')
    new_df["IC50"] = pd.to_numeric(new_df["IC50"], errors="coerce")
    top10 = new_df.nsmallest(10, "IC50")
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=top10,
        x="Inhibitor_ID",
        y="IC50",
        hue="Pocket_ID",
        palette=pocket_palette
    )

    plt.title("IC50 Values of Top Inhibitors ("+unique_variants[i]+")")
    plt.ylabel("IC50 (nM)")
    plt.xlabel("Inhibitor")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("Top_Inhibitors_IC50_barplot"+unique_variants[i]+".png", dpi=300)
    top10.to_csv(unique_variants[i]+"_top10.csv", index=False)
    new_df.to_csv(unique_variants[i]+".csv", index=False)
#print(len(unique_variants))
Results_CSV["IC50"] = pd.to_numeric(Results_CSV["IC50"], errors="coerce")
inhibitor_means = Results_CSV.groupby("Inhibitor_ID")["IC50"].mean().sort_values()
print(inhibitor_means)
#top10_inhibitors = inhibitor_means.head(10)
#top10_df = Results_CSV[Results_CSV["Inhibitor_ID"].isin(top10_inhibitors.index)]
#top10_df.to_csv("top10_global_inhibitors.csv", index=False)
ordered_pockets = ["pocket"+str(i) for i in range(len(unique_pockets))]
