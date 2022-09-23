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

def generate_works_per_year_graphic(researchers, min_year, max_year):
    all_works_per_year = np.array(extract_all_works_years(researchers))
    all_works_per_year.sort()
    aux_list = []

    all_works_per_year = [eval(i) for i in all_works_per_year]

    if min_year and max_year != 0:
        for year in all_works_per_year:
            if not (year > max_year or year < min_year):
                aux_list.append(year)
        all_works_per_year = aux_list.copy()

    elif max_year != 0:
        for year in all_works_per_year:
            if not year > max_year:
                aux_list.append(year)
        all_works_per_year = aux_list.copy()

    elif min_year != 0:
        for year in all_works_per_year:
            if not year < min_year:
                aux_list.append(year)
        all_works_per_year = aux_list.copy()


    all_works_per_year = [str(i) for i in all_works_per_year]

    unique_all_works_per_year = []
    all_works_per_year_count = []

    for x in all_works_per_year:
        if x not in unique_all_works_per_year:
            unique_all_works_per_year.append(x)
            all_works_per_year_count.append(0)

    for x in all_works_per_year:
        index = unique_all_works_per_year.index(x)
        all_works_per_year_count[index] += 1


    fig, ax = plt.subplots(figsize=(len(unique_all_works_per_year), max(all_works_per_year_count) * 0.8))
    ax.bar(unique_all_works_per_year, all_works_per_year_count, edgecolor="black")
    for i in range(len(unique_all_works_per_year)):
        ax.text(i, all_works_per_year_count[i], all_works_per_year_count[i], ha="center")

    plt.xlabel('Anos')
    plt.ylabel('Número de Trabalhos')

    return fig, len(all_works_per_year)

def generate_articles_per_year_graphic(researchers):
    all_articles_year = np.array(extract_all_articles_years(researchers))
    all_articles_year.sort()

    unique_all_articles_per_year = []
    all_articles_per_year_count = []

    for x in all_articles_year:
        if x not in unique_all_articles_per_year:
            unique_all_articles_per_year.append(x)
            all_articles_per_year_count.append(0)

    for x in all_articles_year:
        index = unique_all_articles_per_year.index(x)
        all_articles_per_year_count[index] += 1

    fig, ax = plt.subplots(figsize=(len(unique_all_articles_per_year), max(all_articles_per_year_count) * 0.8))
    ax.bar(unique_all_articles_per_year, all_articles_per_year_count, edgecolor="black")
    for i in range(len(unique_all_articles_per_year)):
        ax.text(i, all_articles_per_year_count[i], all_articles_per_year_count[i], ha="center")

    plt.xlabel('Anos')
    plt.ylabel('Número de Artigos')

    return fig

def generate_boards_piechart(researchers):
    all_board_names = ['Bancas de Mestrado', 'Bancas de Doutorado', 'Bancas de Exame de Qualificação', 'Bancas de Graduação']
    all_board_counts = extract_all_board_quantities(researchers)
    all_board_counts = np.array(all_board_counts)

    for count in all_board_counts:
        if count == 0:
            index = all_board_counts.index(count)
            del all_board_counts[index]
            del all_board_names[index]

    fig1 , ax1 = plt.subplots()

    ax1.pie(all_board_counts, labels=all_board_names, autopct=lambda x: '{:.0f}'.format(x*all_board_counts.sum()/100), shadow=True, startangle=90)
    ax1.axis('equal')

    return fig1

def generate_completed_orientations_per_year_graphic(researchers):
    all_orientations_year = np.array(extract_all_completed_orientation_years(researchers))
    all_orientations_year.sort()

    unique_all_orientations_per_year = []
    all_orientations_per_year_count = []

    for x in all_orientations_year:
        if x not in unique_all_orientations_per_year:
            unique_all_orientations_per_year.append(x)
            all_orientations_per_year_count.append(0)

    for x in all_orientations_year:
        index = unique_all_orientations_per_year.index(x)
        all_orientations_per_year_count[index] += 1

    fig, ax = plt.subplots(figsize=(len(unique_all_orientations_per_year), max(all_orientations_per_year_count) * 0.8))
    ax.bar(unique_all_orientations_per_year, all_orientations_per_year_count, edgecolor="black")
    for i in range(len(unique_all_orientations_per_year)):
        ax.text(i, all_orientations_per_year_count[i], all_orientations_per_year_count[i], ha="center")

    plt.xlabel('Anos')
    plt.ylabel('Número de Orientações Conlcuidas')

    return fig

def generate_in_progress_orientations_per_year_graphic(researchers):
    all_orientations_year = np.array(extract_all_in_progress_orientation_years(researchers))
    all_orientations_year.sort()

    unique_all_orientations_per_year = []
    all_orientations_per_year_count = []

    for x in all_orientations_year:
        if x not in unique_all_orientations_per_year:
            unique_all_orientations_per_year.append(x)
            all_orientations_per_year_count.append(0)

    for x in all_orientations_year:
        index = unique_all_orientations_per_year.index(x)
        all_orientations_per_year_count[index] += 1

    fig, ax = plt.subplots(figsize=(len(unique_all_orientations_per_year), max(all_orientations_per_year_count) * 0.8))
    ax.bar(unique_all_orientations_per_year, all_orientations_per_year_count, edgecolor="black")
    for i in range(len(unique_all_orientations_per_year)):
        ax.text(i, all_orientations_per_year_count[i], all_orientations_per_year_count[i], ha="center")

    plt.xlabel('Anos')
    plt.ylabel('Número de Orientações em Progresso')

    return fig

def extract_all_citations(researchers):
    all_author_names = []

    for researcher in researchers:
        all_author_names.append(researcher.name)

    return all_author_names

def extract_all_works_years(researchers):
    all_works_years_names = []

    if isinstance(researchers, list):
            for researcher in researchers:
                all_works_years_names = all_works_years_names + researcher.works_years
    else:
        all_works_years_names = researchers.works_years

    return all_works_years_names

def extract_all_articles_years(researchers):
    all_articles_years_names = []

    if isinstance(researchers, list):
            for researcher in researchers:
                all_articles_years_names = all_articles_years_names + researcher.articles
    else:
        all_articles_years_names = researchers.articles

    return all_articles_years_names

def extract_all_board_quantities(researchers):
    all_board_quantities = [0, 0, 0, 0]

    if isinstance(researchers, list):
            for researcher in researchers:
                for board in researcher.board:
                    if board == 'Bancas de Mestrado':
                        all_board_quantities[0] += researcher.board_quantity[researcher.board.index('Bancas de Mestrado')]

                    if board == 'Bancas de Doutorado':
                        all_board_quantities[1] += researcher.board_quantity[researcher.board.index('Bancas de Doutorado')]

                    if board == 'Bancas de Exame de Qualificação':
                        all_board_quantities[2] += researcher.board_quantity[researcher.board.index('Bancas de Exame de Qualificação')]

                    if board == 'Bancas de Graduação':
                        all_board_quantities[3] += researcher.board_quantity[researcher.board.index('Bancas de Graduação')]
    else:
        for board in researchers.board:
            if board == 'Bancas de Mestrado':
                all_board_quantities[0] += researchers.board_quantity[researchers.board.index('Bancas de Mestrado')]

            if board == 'Bancas de Doutorado':
                all_board_quantities[1] += researchers.board_quantity[researchers.board.index('Bancas de Doutorado')]

            if board == 'Bancas de Exame de Qualificação':
                all_board_quantities[2] += researchers.board_quantity[researchers.board.index('Bancas de Exame de Qualificação')]

            if board == 'Bancas de Graduação':
                all_board_quantities[3] += researchers.board_quantity[researchers.board.index('Bancas de Graduação')]

    return all_board_quantities

def extract_all_completed_orientation_years(researchers):
    all_completed_orientation_names = []

    if isinstance(researchers, list):
            for researcher in researchers:
                all_completed_orientation_names = all_completed_orientation_names + researcher.completed_orientations
    else:
        all_completed_orientation_names = researchers.completed_orientations

    return all_completed_orientation_names

def extract_all_in_progress_orientation_years(researchers):
    all_in_progress_orientation_names = []

    if isinstance(researchers, list):
            for researcher in researchers:
                all_in_progress_orientation_names = all_in_progress_orientation_names + researcher.in_progress_orientations
    else:
        all_in_progress_orientation_names = researchers.in_progress_orientations

    return all_in_progress_orientation_names