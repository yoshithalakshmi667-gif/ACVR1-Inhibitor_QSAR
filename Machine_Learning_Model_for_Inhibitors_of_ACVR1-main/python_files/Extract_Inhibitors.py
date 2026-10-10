import requests
from bs4 import BeautifulSoup
import regex as re
import pymol
import os

def fetch_structures(ligands_ids, OutputFolder):
    pymol.pymol_argv = ['pymol', '-c']
    pymol.finish_launching()

    for pdb_id, ligand_id in ligands_ids.items():
        try:
            print(f"Fetching PDB ID: {pdb_id}")

            pymol.cmd.fetch(pdb_id, "structure", type="pdb")

            pymol.cmd.select("inhibitor", f"resn {ligand_id} and chain A")

            pymol.cmd.remove(f"not inhibitor")

            output_folder = os.path.join(OutputFolder, f'{pdb_id}_{ligand_id}.pdb')

            pymol.cmd.save(output_folder, "inhibitor")

            pymol.cmd.delete("all")

        except Exception as e:
            print(f"Error processing {pdb_id}: {e}")

    pymol.cmd.quit()

    '''code_directory = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(FilesDirectory, exist_ok=True)
    os.makedirs(OutputFolder, exist_ok=True)

    for files in os.listdir(code_directory):
        if files.endswith(".pdb"):
            file_path = os.path.join(code_directory, files)
            polymers_n_inhibitors = os.path.join(FilesDirectory, files)
            os.rename(file_path, polymers_n_inhibitors)'''

url = "https://search.rcsb.org/rcsbsearch/v2/query"

query = {
    "query": {
        "type": "terminal",
        "service": "text",
        "parameters": {
            "attribute": "struct.title",
            "operator": "contains_phrase",
            "value": "ACVR1"
        }
    },
    "return_type": "entry",
    "request_options": {
        "paginate": {"start": 0, "rows": 100},
        "results_content_type": ["experimental"],
        "sort": [{"sort_by": "score", "direction": "desc"}]
    }
}

response = requests.post(url, json=query)

if response.status_code == 200:
    data = response.json()
    pdb_ids = [entry['identifier'] for entry in data.get('result_set', [])]

def extract_inhibitors_IDs(PDB_IDs):
    ligands_ids = {}
    for id in PDB_IDs:
        url = f'https://www.rcsb.org/structure/{id}'
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            ligand_id = re.findall(r"href\=\"\/ligand\-validation\/" + id + "\/([0-9A-Z]+)\"\>Ligands\<", str(soup))
        #print(id)
        #print(ligand_id)
            ligands_ids[id] = ligand_id[0]
    return ligands_ids

ligands_ids = extract_inhibitors_IDs(pdb_ids)
fetch_structures(ligands_ids, '/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/Only_Inhibitors')
