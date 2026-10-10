# Integrative Prediction of ACVR1 Inhibitor Potency for Fibrodysplasia Ossificans Progressiva and Diffuse Intrinsic Pontine Glioma Using Variant- and Pocket-Aware QSAR

## Overview

This project integrates structural bioinformatics, molecular docking, cheminformatics, and machine learning to investigate potential inhibitors of Activin A Receptor Type I (ACVR1/ALK2), a serine/threonine kinase associated with Fibrodysplasia Ossificans Progressiva (FOP) and diffuse intrinsic pontine glioma (DIPG). Since mutations in ACVR1 can alter protein structure and ligand interactions, this project uses a variant- and binding-pocket-aware computational pipeline to investigate differences in predicted inhibitor potency.

The workflow combines ACVR1 protein structure retrieval, generation of 13 protein variants, binding-pocket prediction, automated molecular docking, molecular descriptor calculation, and machine learning-based QSAR modeling. An initial set of 98 inhibitors was used for docking and model development, followed by a virtual-screening workflow involving approximately 1,000 candidate compounds retrieved from PubChem. Molecular dynamics simulations were also performed for selected ACVR1 systems to further investigate protein–ligand interactions.

## Repository Structure

```text
ACVR1-Inhibitor-Prediction/
├── README.md
├── python_files/        # All Python scripts: structure/ligand extraction, variant
│                        # generation, SMILES retrieval, Open Babel conversion,
│                        # P2Rank, docking automation, dataset creation, MLP training
├── Variants/            # Wild-type and the 13 generated ACVR1 variant structures
├── Inhibitors/          # Inhibitor 3D structures (PDB/PDBQT) and SMILES files
├── P2rank_Results/      # P2Rank binding-pocket prediction outputs (CSV)
├── Docking_Results/     # AutoDock Vina configs, logs, poses, and parsed affinity scores
└── Training_Dataset/    # RDKit descriptor tables and docking-derived potency
                         # estimates used to train and test the QSAR model
```

### Python scripts (`python_files/`)

| Pipeline step | Script(s) |
|---|---|
| Download ACVR1 structures and isolate ligands | `Extract_Ligands.py`, `Unique_Inhibitors.py` |
| Generate ACVR1 variants (PyMOL mutagenesis) | `Create_ACVR1_Variants` |
| Retrieve inhibitor SMILES from PubChem | `getSMILES.py` |
| Build 3D inhibitor structures with Open Babel | `Run_OpenBabel.py` |
| Predict binding pockets | `Run_P2Rank.py` |
| Prepare docking inputs and run docking | `PDB_2_PDBQT.py`, `Create_ConfigFiles.py`, `Run_AutoDockVina.py` |
| Build QSAR training dataset | `Create_Docking_Results_csv.py` |
| Train the MLP regressor | `Train_MLP.py` |
| Prepare the virtual-screening test dataset | `Prepare_Test_Dataset.py` |

## Pipeline

**1. Protein Structure Retrieval and Variant Generation (RCSB PDB and PyMOL)**

ACVR1 protein structures were retrieved from the RCSB Protein Data Bank (PDB) through its API using the keyword "ACVR1", and fetched with command-line PyMOL. PyMOL was used to generate 13 ACVR1 variants through structure-based mutagenesis (for example, reverting R206H to obtain a wild-type structure). MAFFT was used to align protein sequences and verify that each variant differed at the expected position. These structures provided the basis for investigating variant-specific inhibitor interactions.

**2. Inhibitor Collection and Structure Preparation (PDB, PubChem and Open Babel)**

Inhibitor 3D structures (69 initially, with duplicates removed) were isolated from the downloaded PDB complexes. To expand the inhibitor set, SMILES strings of compounds reported against ACVR1 were extracted from PubChem using Selenium, BeautifulSoup, and regular expressions, and converted into 3D structures with Open Babel. This produced a total of 98 inhibitor structures for docking.

The complete selection criteria for these compounds were not fully documented, so the dataset should be interpreted as the inhibitor set used in the computational analysis rather than a systematically defined experimental potency benchmark.

**3. Binding-Pocket Prediction (P2Rank)**

P2Rank was used to predict potential ligand-binding pockets in the ACVR1 structures. Seven candidate pockets were reported across the analyzed structures. The predicted pocket coordinates were used to define the docking search space, enabling comparison of predicted binding across variants and pockets.

**4. Automated Molecular Docking (AutoDock Vina)**

Protein and ligand structures were converted to PDBQT format (Open Babel and AutoDock Tools, including Kollman charges and AutoDock-4 atom types). A configuration file was generated for every variant–inhibitor–pocket combination, and AutoDock Vina runs were automated with Python's Subprocess library on the BioLinux machines in the UTEP Bioinformatics Laboratory. Docking results were parsed and organized into CSV files to support downstream comparisons.

Docking affinity scores, expressed in kcal/mol, were used to compare predicted protein–ligand binding interactions. More negative scores indicate more favorable predicted binding according to the Vina scoring function, but do not independently establish experimental binding or inhibition.

**5. Docking-Derived Potency Estimation**

The best binding affinity for each variant–inhibitor–pocket combination was converted into an approximate Ki/IC50-like value using a thermodynamic relationship (R = 1.987×10⁻³ kcal/mol·K, T = 298 K). These values were treated as computational estimates rather than experimentally measured IC50 values, and served as target values for the machine learning workflow. Inhibitors were ranked per variant using a score combining mean estimated potency and its standard deviation across pockets.

**6. Molecular Descriptor Calculation (RDKit)**

RDKit was used to calculate numerical molecular descriptors for the inhibitor compounds, including:

- Molecular weight
- LogP (lipophilicity)
- Topological polar surface area (TPSA)
- Hydrogen-bond donors and acceptors
- Rotatable bond count
- Quantitative Estimate of Drug-likeness (QED)
- Lipinski rule-of-five pass/fail

These descriptors were used as input features for the QSAR modeling and virtual-screening workflow.

**7. Machine Learning-Based QSAR Modeling (Scikit-learn MLP Regressor)**

A Multilayer Perceptron (MLP) regression model was implemented using scikit-learn to learn relationships between molecular descriptors and docking-derived potency estimates. The workflow included 91 training datasets associated with ACVR1 variant–pocket combinations, each containing features for the 98 inhibitors. PCA was incorporated into feature processing to reduce dimensionality, and the MLP was trained for up to 1,000 iterations.

The model's predictions reflect patterns learned from computationally derived training values. They should not be interpreted as experimentally validated IC50 measurements. Independent model validation and experimental activity data are needed to establish predictive reliability.

**8. Virtual Screening of Additional Compounds (PubChem and QSAR Model)**

Approximately 1,000 candidate compounds were retrieved from PubChem using the search keyword "kinase inhibitor," reflecting the kinase activity of ACVR1. Descriptors were calculated with RDKit for each variant–pocket combination, and the trained QSAR model was applied to prioritize molecules with favorable predicted activity.

The available project report does not establish that all 1,000 candidates were subjected to a second AutoDock Vina docking run. Therefore, the additional-compound analysis is described as model-based virtual screening rather than confirmed redocking of every candidate.

**9. Molecular Dynamics Analysis**

Molecular dynamics analyses were performed for selected ACVR1 systems involving wild-type ACVR1 and the R206H, G328V, and R258G variants, with Lestaurtinib investigated as a ligand. This stage extended the structural analysis beyond static docking poses to investigate protein–ligand behavior. Quantitative simulation metrics should be reported alongside these results when available.

## Key Results

| **Analysis** | **Reported Finding** | **Interpretation** |
|---|---|---|
| ACVR1 variant generation | 13 variants generated | Enabled comparative analysis of variant-specific inhibitor interactions |
| Binding-pocket prediction | 7 candidate pockets reported | Supported pocket-aware docking analysis |
| Initial inhibitor dataset | 98 compounds | Used in the reported docking and modeling workflow |
| Machine learning datasets | 91 variant–pocket training datasets reported | Supported variant- and pocket-specific regression modeling |
| Docking-based inhibitor ranking | Lestaurtinib emerged as a leading inhibitor | Identified a candidate for further computational investigation |
| Pocket comparison | Pockets 1, 3, and 4 were reported as more favorable | Suggested differences in predicted binding favorability between pockets |
| Variant comparison | G325A was reported as less favorable across inhibitors | Suggested variant-dependent differences in predicted binding |
| Additional candidate screening | Approximately 1,000 PubChem compounds collected | Expanded the candidate space for model-based screening |

**Lestaurtinib** (CHEMBL603469) emerged as a leading inhibitor in the reported docking-derived comparisons across ACVR1 variants. This result identifies a candidate for further investigation but does not establish experimentally confirmed inhibition or therapeutic efficacy.

The analysis also indicated that predicted inhibitor rankings varied across ACVR1 variants and binding pockets. Pockets 1, 3, and 4 were reported as comparatively favorable, while G325A showed less favorable predicted interactions across the analyzed inhibitors. These observations illustrate the potential value of incorporating protein variants and binding-pocket information into computational inhibitor prioritization.

Additional compounds, including Linifanib, Temsirolimus, and Dovitinib Lactate, were identified by the QSAR model among the candidates discussed in the report (for example, Temsirolimus for R206H, Linifanib for G356D and R202I, and Dovitinib Lactate for G325A). Their predicted relevance should be interpreted within the limitations of the computational screening workflow.

All docking scores, calculated potency estimates, machine learning predictions, and molecular dynamics interpretations are computational results. Experimental binding assays, biochemical inhibition studies, and independent model validation are required to establish biological relevance.

## Tools Used

- [RCSB Protein Data Bank](https://www.rcsb.org/) — protein structure retrieval
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/) — chemical information and compound SMILES
- [PyMOL](https://pymol.org/) — protein structure visualization and mutagenesis
- [MAFFT](https://mafft.cbrc.jp/alignment/software/) — protein sequence alignment
- [P2Rank](https://github.com/rdk/p2rank) — protein ligand-binding pocket prediction
- [AutoDock Vina](https://vina.scripps.edu/) — molecular docking and binding affinity estimation
- [AutoDock Tools](https://ccsb.scripps.edu/mgltools/) — PDBQT preparation (Kollman charges, atom typing)
- [Open Babel](https://openbabel.org/) — chemical structure conversion and preparation
- [RDKit](https://www.rdkit.org/) — molecular descriptor calculation and cheminformatics
- [scikit-learn](https://scikit-learn.org/) — MLP regression, PCA, and machine learning
- [Python](https://www.python.org/) (pandas, matplotlib, seaborn) — workflow automation, data extraction, and analysis
- [Selenium](https://www.selenium.dev/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) — web data extraction

## Limitations

- Docking scores approximate binding favorability and do not directly demonstrate biological inhibition.
- Docking-derived potency estimates are not equivalent to experimentally measured IC50 values.
- The model was trained using computationally derived estimates, which may propagate limitations of the docking and potency-estimation procedures.
- The complete inhibitor-selection criteria, model architecture, PCA configuration, and model validation metrics are not fully specified in the available report.
- The available documentation does not confirm that all 1,000 additional compounds underwent a second docking run.
- Molecular dynamics simulations alone cannot establish biological efficacy or therapeutic suitability.
- Predicted compounds require independent computational assessment and experimental validation.

## Future Directions

- Evaluate model performance using independent test compounds and experimentally measured ACVR1 inhibitor activity.
- Document model architecture, train/test splitting, cross-validation, and regression metrics.
- Perform secondary docking for prioritized compounds where appropriate.
- Investigate variant-specific protein–ligand interactions using quantitative structural and molecular dynamics metrics.
- Expand the training dataset using experimentally characterized inhibitors.
- Explore model interpretability to identify molecular properties associated with predicted inhibitor activity.
- Experimentally validate promising candidates for binding affinity, selectivity, and biochemical inhibition.

## References

- RCSB Protein Data Bank. https://www.rcsb.org/
- Kim, S., Chen, J., Cheng, T., et al. PubChem 2023 update. *Nucleic Acids Research*. 2023;51(D1):D1373–D1380.
- Trott, O., & Olson, A. J. (2010). AutoDock Vina: Improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading. *Journal of Computational Chemistry*, 31(2), 455–461.
- Eberhardt, J., Santos-Martins, D., Tillack, A. F., & Forli, S. (2021). AutoDock Vina 1.2.0: New docking methods, expanded force field, and Python bindings. *Journal of Chemical Information and Modeling*, 61(8), 3891–3898.
- RDKit. Open-source cheminformatics software. https://www.rdkit.org/
- scikit-learn. Machine learning in Python. https://scikit-learn.org/
- MAFFT. Multiple sequence alignment software. https://mafft.cbrc.jp/alignment/software/
- P2Rank. Protein ligand-binding site prediction. https://github.com/rdk/p2rank

## Acknowledgments

We would like to thank Dr. Jonathon Mohl and Amanda Batayckan for guiding us through this project and for always being available for our questions. Docking simulations were run on the BioLinux machines at the University of Texas at El Paso's Bioinformatics Laboratory.

## Authors

Victor Emmanuel Rodriguez Torres, Sasha G. Soto, Valeria Chavira, Umme Tania, and **Yoshitha Evuri**

M.S. Bioinformatics and Computational Biology  
The University of Texas at El Paso

**Research Interests:** Computational Drug Discovery · Structural Bioinformatics · Molecular Docking · QSAR · Machine Learning · Protein–Ligand Interactions · Cancer Bioinformatics
