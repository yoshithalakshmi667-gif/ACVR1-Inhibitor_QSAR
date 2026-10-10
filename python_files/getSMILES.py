from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import regex as re
from bs4 import BeautifulSoup
import requests
import json
from rdkit import Chem

driver = webdriver.Safari()

url = "https://www.ebi.ac.uk/chembl/explore/activities/STATE_ID:VD-jnocmN-pdYaU9dDXxsA%3D%3D"
driver.get(url)

try:
    dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'v-select__selections')]"))
    )
    dropdown.click()
    time.sleep(2)

    option_100 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'v-list-item') and text()='100']"))
    )
    option_100.click()
    time.sleep(5)

    html_content = driver.page_source

    CHEM_IDS = re.findall(r"href\=\"https\:\/\/www\.ebi\.ac\.uk\/chembl\/explore\/compound\/(CHEMBL[0-9]+)\"", html_content)

    #print(CHEM_IDS)

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()

CHEMID_n_SMILE = {}
for ID in CHEM_IDS:
    url = f"https://www.ebi.ac.uk/chembl/explore/compound/{ID}"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        str_soup = str(soup)
        #print(str_soup)
        if re.search(r"\,smiles\:\"([a-zA-Z0-9\(\)\\\=\[\]\#]+)", str_soup):
            #print(ID)
            match1 = re.search(r"\,smiles\:\"([a-zA-Z0-9\(\)\\\=\[\]\#\-\@\+]+)", str_soup)
            #print(match1.group(1))
            match2 = re.search(r"([a-zA-Z0-9\(\)\\\=\[\]\#\-\@\+]+)\"\,monoisotopicMolecularWeight\:", str_soup)
            #print(match2.group(1))
            if match1.group(1) == match2.group(1):
                encode_SMILE = match1.group(1)
            else:
                encode_SMILE = match1.group(1) + match2.group(1)

            decode_SMILE = json.loads(f'"{encode_SMILE}"')
            CHEMID_n_SMILE[ID] = decode_SMILE
        else:
            #print(ID)
            #print("Check if SMILE is available.")
            pass
#print(CHEMID_n_SMILE)

with open("/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/Analysis_and Modeling_of_Biological_Structures/Project/SMILES/Inhibitor_SMILES.smi", "w") as SMILES_File:
    for CHEMID, SMILE in CHEMID_n_SMILE.items():
        SMILES_File.write(f"{SMILE}\t{CHEMID}\n")