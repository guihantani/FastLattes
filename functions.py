import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from researcher import Researcher
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from itertools import chain
from operator import methodcaller

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


def generate_articles_per_year_graphic(researchers, min_year, max_year):
    all_articles_year = np.array(extract_all_articles_years(researchers))
    all_articles_year.sort()
    aux_list = []

    all_articles_year = [eval(i) for i in all_articles_year]

    if min_year and max_year != 0:
        for year in all_articles_year:
            if not (year > max_year or year < min_year):
                aux_list.append(year)
        all_articles_year = aux_list.copy()

    elif max_year != 0:
        for year in all_articles_year:
            if not year > max_year:
                aux_list.append(year)
        all_articles_year = aux_list.copy()

    elif min_year != 0:
        for year in all_articles_year:
            if not year < min_year:
                aux_list.append(year)
        all_articles_year = aux_list.copy()

    all_articles_year = [str(i) for i in all_articles_year]

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


def generate_boards_piechart(researchers, min_year, max_year):
    all_board_names = ['Bancas de Mestrado', 'Bancas de Tese de Doutorado', 'Bancas de Qualificação de Doutorado', 'Bancas de Graduação']
    all_boards = extract_all_boards(researchers)
    aux_all_boards = {'Bancas de Mestrado': [], 'Bancas de Tese de Doutorado': [] ,'Bancas de Qualificação de Doutorado': [], 'Bancas de Graduação': []}
    all_board_counts = []

    for board in all_board_names:
        if min_year and max_year != 0:
            for year in all_boards[board]:
                if not (int(year) > max_year or int(year) < min_year):
                    aux_all_boards[board].append(year)
            all_boards[board] = aux_all_boards[board].copy()

        elif max_year != 0:
            for year in all_boards[board]:
                if not int(year) > max_year:
                    aux_all_boards[board].append(year)
            all_boards[board] = aux_all_boards[board].copy()

        elif min_year != 0:
            for year in all_boards[board]:
                if not int(year) < min_year:
                    aux_all_boards[board].append(year)
            all_boards[board] = aux_all_boards[board].copy()

    for board in all_board_names:
        all_board_counts.append(len(all_boards[board]))

    all_board_counts = np.array(all_board_counts)

    fig1 , ax1 = plt.subplots()
    if all(item == 0 for item in all_board_counts):
        return None, None

    plt.title('Número de Participações por Banca')
    ax1.pie(all_board_counts, labels=all_board_names, autopct=lambda p: '{:.2f}%\n({:.0f})'.format(p,(p/100)*all_board_counts.sum()), shadow=True, startangle=90)
    ax1.axis('equal')

    return fig1, all_board_counts


def generate_completed_orientations_per_year_graphic(researchers, min_year, max_year):
    all_orientations_year = np.array(extract_all_completed_orientation_years(researchers))
    all_orientations_year.sort()
    aux_list = []

    all_orientations_year = [eval(i) for i in all_orientations_year]

    if min_year and max_year != 0:
        for year in all_orientations_year:
            if not (year > max_year or year < min_year):
                aux_list.append(year)
        all_orientations_year = aux_list.copy()

    elif max_year != 0:
        for year in all_orientations_year:
            if not year > max_year:
                aux_list.append(year)
        all_orientations_year = aux_list.copy()

    elif min_year != 0:
        for year in all_orientations_year:
            if not year < min_year:
                aux_list.append(year)
        all_orientations_year = aux_list.copy()

    all_orientations_year = [str(i) for i in all_orientations_year]

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


def generate_in_progress_orientations_per_year_graphic(researchers, min_year, max_year):
    all_orientations_year = np.array(extract_all_in_progress_orientation_years(researchers))
    all_orientations_year.sort()
    aux_list = []

    all_orientations_year = [eval(i) for i in all_orientations_year]

    if min_year and max_year != 0:
        for year in all_orientations_year:
            if not (year > max_year or year < min_year):
                aux_list.append(year)
        all_orientations_year = aux_list.copy()

    elif max_year != 0:
        for year in all_orientations_year:
            if not year > max_year:
                aux_list.append(year)
        all_orientations_year = aux_list.copy()

    elif min_year != 0:
        for year in all_orientations_year:
            if not year < min_year:
                aux_list.append(year)
        all_orientations_year = aux_list.copy()

    all_orientations_year = [str(i) for i in all_orientations_year]

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


def extract_all_boards(researchers):
    finalBoard = defaultdict(list)
    listOfBoards = []

    if isinstance(researchers, list):
        for researcher in researchers:
            listOfBoards.append(researcher.board)

        dict_items = map(methodcaller('items'), listOfBoards)
        for k, v in chain.from_iterable(dict_items):
            finalBoard[k].extend(v)

        return finalBoard

    else:
        return researchers.board


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