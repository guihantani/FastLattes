import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import wordcloud
from researcher import Researcher
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from itertools import chain
from operator import methodcaller
from wordcloud import WordCloud
import nltk

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

    if all_works_per_year_count == []:
        return None

    fig, ax = plt.subplots(figsize=(len(unique_all_works_per_year)/2, max(all_works_per_year_count) * (len(unique_all_works_per_year) * 0.015)))
    ax.bar(unique_all_works_per_year, all_works_per_year_count, edgecolor="black")
    fig.patch.set_facecolor((0.14,0.17,0.23))
    ax.set_facecolor((0.14,0.17,0.23))
    ax.tick_params(axis='x', colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color((0.14,0.17,0.23))
    ax.spines['right'].set_color((0.14,0.17,0.23))
    ax.spines['left'].set_color((0.14,0.17,0.23))
    ax.get_yaxis().set_visible(False)
    for i in range(len(unique_all_works_per_year)):
        ax.text(i, all_works_per_year_count[i] + 0.1, all_works_per_year_count[i], ha="center", color='white')

    fig.autofmt_xdate()
    plt.xlabel('Anos', color='white')


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

    if all_articles_per_year_count == []:
        return None

    fig, ax = plt.subplots(figsize=(len(unique_all_articles_per_year)/2, max(all_articles_per_year_count) * (len(unique_all_articles_per_year) * 0.015)))
    fig.patch.set_facecolor((0.14, 0.17, 0.23))
    ax.set_facecolor((0.14, 0.17, 0.23))
    ax.tick_params(axis='x', colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color((0.14, 0.17, 0.23))
    ax.spines['right'].set_color((0.14, 0.17, 0.23))
    ax.spines['left'].set_color((0.14, 0.17, 0.23))
    ax.get_yaxis().set_visible(False)
    ax.bar(unique_all_articles_per_year, all_articles_per_year_count, edgecolor="black")
    for i in range(len(unique_all_articles_per_year)):
        ax.text(i, all_articles_per_year_count[i] + 0.1, all_articles_per_year_count[i], ha="center", color='white')

    fig.autofmt_xdate()
    plt.xlabel('Anos', color='white')

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
    fig1.patch.set_facecolor((0.14, 0.17, 0.23))
    ax1.set_facecolor((0.14, 0.17, 0.23))
    if all(item == 0 for item in all_board_counts):
        return None, None

    plt.title('Número de Participações por Banca', color='white')
    ax1.pie(all_board_counts, labels=all_board_names, autopct=lambda p: '{:.2f}%\n({:.0f})'.format(p,(p/100)*all_board_counts.sum()), shadow=True, startangle=90, textprops={'color':"w"})
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

    if all_orientations_per_year_count == []:
        return None

    fig, ax = plt.subplots(figsize=(len(unique_all_orientations_per_year)/2, max(all_orientations_per_year_count) * (len(unique_all_orientations_per_year) * 0.015)))
    fig.patch.set_facecolor((0.14, 0.17, 0.23))
    ax.set_facecolor((0.14, 0.17, 0.23))
    ax.tick_params(axis='x', colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color((0.14, 0.17, 0.23))
    ax.spines['right'].set_color((0.14, 0.17, 0.23))
    ax.spines['left'].set_color((0.14, 0.17, 0.23))
    ax.get_yaxis().set_visible(False)
    ax.bar(unique_all_orientations_per_year, all_orientations_per_year_count, edgecolor="black")
    for i in range(len(unique_all_orientations_per_year)):
        ax.text(i, all_orientations_per_year_count[i] + 0.1, all_orientations_per_year_count[i], ha="center", color='white')

    fig.autofmt_xdate()
    plt.xlabel('Anos', color='white')

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

    if all_orientations_per_year_count == []:
        return None

    fig, ax = plt.subplots(figsize=(len(unique_all_orientations_per_year)/2, max(all_orientations_per_year_count) * (len(unique_all_orientations_per_year) * 0.015)))
    fig.patch.set_facecolor((0.14, 0.17, 0.23))
    ax.set_facecolor((0.14, 0.17, 0.23))
    ax.tick_params(axis='x', colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color((0.14, 0.17, 0.23))
    ax.spines['right'].set_color((0.14, 0.17, 0.23))
    ax.spines['left'].set_color((0.14, 0.17, 0.23))
    ax.get_yaxis().set_visible(False)
    ax.bar(unique_all_orientations_per_year, all_orientations_per_year_count, edgecolor="black")
    for i in range(len(unique_all_orientations_per_year)):
        ax.text(i, all_orientations_per_year_count[i] + 0.1, all_orientations_per_year_count[i], ha="center", color='white')

    fig.autofmt_xdate()
    plt.xlabel('Anos', color='white')


    return fig


def generate_projects_piechart(researchers, min_year, max_year):
    all_projects_names = ['Projetos de Pesquisa', 'Projetos de Extensão', 'Projetos de Ensino', 'Projetos de Desenvolvimento', 'Outros Projetos']
    all_projects = extract_all_projects(researchers)
    aux_all_projects = {'Projetos de Pesquisa': [], 'Projetos de Extensão': [], 'Projetos de Ensino': [], 'Projetos de Desenvolvimento': [], 'Outros Projetos': []}
    all_projects_counts = []

    for project in all_projects_names:
        if min_year and max_year != 0:
            for year in all_projects[project]:
                if not (int(year) > max_year or int(year) < min_year):
                    aux_all_projects[project].append(year)
            all_projects[project] = aux_all_projects[project].copy()

        elif max_year != 0:
            for year in all_projects[project]:
                if not int(year) > max_year:
                    aux_all_projects[project].append(year)
            all_projects[project] = aux_all_projects[project].copy()

        elif min_year != 0:
            for year in all_projects[project]:
                if not int(year) < min_year:
                    aux_all_projects[project].append(year)
            all_projects[project] = aux_all_projects[project].copy()

    for project in all_projects_names:
        all_projects_counts.append(len(all_projects[project]))

    all_projects_counts = np.array(all_projects_counts)

    fig1 , ax1 = plt.subplots()
    fig1.patch.set_facecolor((0.14, 0.17, 0.23))
    ax1.set_facecolor((0.14, 0.17, 0.23))
    if all(item == 0 for item in all_projects_counts):
        return None, None

    plt.title('Número de Participações em Projetos', color='white')
    ax1.pie(all_projects_counts, labels=all_projects_names, autopct=lambda p: '{:.2f}%\n({:.0f})'.format(p,(p/100)*all_projects_counts.sum()), shadow=True, startangle=90, textprops={'color':"w"})
    ax1.axis('equal')

    return fig1, all_projects_counts

def generate_word_cloud(researcher):
    fig1, ax1 = plt.subplots()
    portuguese_stop_words = list(nltk.corpus.stopwords.words('portuguese'))
    english_stop_words = list(wordcloud.STOPWORDS)
    stop_words = portuguese_stop_words + english_stop_words
    word_cloud = WordCloud(
        width=3000,
        height=2000,
        random_state=1,
        background_color="salmon",
        colormap="Pastel1",
        collocations=False,
        stopwords=stop_words,
        min_word_length=2
    ).generate(researcher.words)

    plt.title('Nuvem de Palavra de todos os Trabalhos e Artigos')
    plt.imshow(word_cloud)
    plt.axis("off")

    return fig1

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


def extract_all_projects(researchers):
    final_project = defaultdict(list)
    list_of_projects = []

    if isinstance(researchers, list):
        for researcher in researchers:
            list_of_projects.append(researcher.projects)

        dict_items = map(methodcaller('items'), list_of_projects)
        for k, v in chain.from_iterable(dict_items):
            final_project[k].extend(v)

        return final_project

    else:
        return researchers.projects

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