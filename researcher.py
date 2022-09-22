class Researcher:
  def __init__(self, root):
    self.name = root.find('DADOS-GERAIS').attrib['NOME-COMPLETO']
    self.works_years = []
    self.articles = []
    self.orcid = None
    self.address = None
    self.institution = None

    #Works in events
    if len(root[1]) != 0:
      for work_year in root.find('PRODUCAO-BIBLIOGRAFICA').find('TRABALHOS-EM-EVENTOS').findall('TRABALHO-EM-EVENTOS'):
        self.works_years.append(work_year.find('DADOS-BASICOS-DO-TRABALHO').attrib['ANO-DO-TRABALHO'])

    #Articles
    if root.find('PRODUCAO-BIBLIOGRAFICA').find('ARTIGOS-PUBLICADOS') != None:
      for work_year in root.find('PRODUCAO-BIBLIOGRAFICA').find('ARTIGOS-PUBLICADOS').findall('ARTIGO-PUBLICADO'):
        self.articles.append(work_year.find('DADOS-BASICOS-DO-ARTIGO').attrib['ANO-DO-ARTIGO'])

    #Orcid
    if 'ORCID-ID' in root.find('DADOS-GERAIS').attrib:
      self.orcid = root.find('DADOS-GERAIS').attrib['ORCID-ID']

    #Researcher Address
    if 'PAIS' in root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib:
      self.address = root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib['PAIS']

    if 'CIDADE' in root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib:
      self.address += ', ' + root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib['CIDADE']

    if 'BAIRRO' in root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib:
      self.address += ', ' + root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib['BAIRRO']

    if 'LOGRADOURO-COMPLEMENTO' in root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib:
      self.address += ', ' + root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib['LOGRADOURO-COMPLEMENTO']

    #Institution
    if 'NOME-INSTITUICAO-EMPRESA' in root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib:
      self.institution = root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib['NOME-INSTITUICAO-EMPRESA']

    if 'NOME-ORGAO' in root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib:
      self.institution = ' - ' + root.find('DADOS-GERAIS').find('ENDERECO').find('ENDERECO-PROFISSIONAL').attrib['NOME-ORGAO']