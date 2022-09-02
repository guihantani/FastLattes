import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from researcher import Researcher
import matplotlib.pyplot as plt
import numpy as np

def initialize_researchers(path):
    name_of_all_zip_files = os.listdir(path + '/.')
    researchers = []

    for file in name_of_all_zip_files:
        os.chdir(path)
        with ZipFile(file, 'r') as z:
            z.extractall()  # unzip file

        file_path = path + '/curriculo.xml'
        xml = ET.parse(file_path).getroot()  # load file
        r = Researcher(xml)
        researchers.append(r)
        os.remove(file_path)  # remove unzip file

    return researchers

def generate_works_per_year_graphic(researchers):
    all_works_per_year = np.array(extract_all_works_years(researchers))
    all_works_per_year.sort()

    unique_all_works_per_year = []
    all_works_per_year_count = []

    for x in all_works_per_year:
        if x not in unique_all_works_per_year:
            unique_all_works_per_year.append(x)
            all_works_per_year_count.append(0)

    for x in all_works_per_year:
        index = unique_all_works_per_year.index(x)
        all_works_per_year_count[index] += 1

    fig, ax = plt.subplots(figsize=(len(unique_all_works_per_year), max(all_works_per_year_count) - 3))
    ax.bar(unique_all_works_per_year, all_works_per_year_count, edgecolor="black")
    for i in range(len(unique_all_works_per_year)):
        ax.text(i, all_works_per_year_count[i], all_works_per_year_count[i], ha="center")

    plt.xlabel('Anos')
    plt.ylabel('Número de Trabalhos')

    return fig

def extract_all_citations(researchers):
    all_author_names = []

    for researcher in researchers:
        all_author_names.append(researcher.name)

    return all_author_names

def extract_all_works_years(researchers):
    all_works_years_names = []

    for researcher in researchers:
        all_works_years_names = all_works_years_names + researcher.works_years

    return all_works_years_names

