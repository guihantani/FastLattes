import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from pip._internal.utils.unpacking import unzip_file
from researcher import Researcher

def extract_authors_from_header(xml):
    r = Researcher(xml)

    return r.name


def extract_all_citations(path):
    name_of_all_zip_files = os.listdir(path + '/.')
    all_author_names = []

    for file in name_of_all_zip_files:
        os.chdir(path)
        with ZipFile(file, 'r') as z:
            z.extractall() # unzip file

        file_path = path + '/curriculo.xml'
        xml = ET.parse(file_path).getroot() # load file
        author = extract_authors_from_header(xml) # extract names
        all_author_names.append(author)
        os.remove(file_path) # remove unzip file

    return all_author_names
