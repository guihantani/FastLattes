class Researcher:
  def __init__(self, root):
    self.name = root.find('DADOS-GERAIS').attrib['NOME-COMPLETO']
    self.works_years = []
    self.articles = []
    self.board = []
    self.board_quantity = []
    self.completed_orientations = []
    self.in_progress_orientations = []
    self.orcid = None
    self.address = None
    self.institution = None

    #Works in events
    if root.find('PRODUCAO-BIBLIOGRAFICA').find('TRABALHOS-EM-EVENTOS') != None:
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

    #Boards
    if root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO') != None:
      if root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO').find('PARTICIPACAO-EM-BANCA-DE-MESTRADO') != None:
        for participation_board in root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO').findall('PARTICIPACAO-EM-BANCA-DE-MESTRADO'):
          if 'Bancas de Mestrado' in self.board:
            self.board_quantity[self.board.index('Bancas de Mestrado')] += 1

          else:
            self.board.append('Bancas de Mestrado')
            self.board_quantity.append(1)

      if root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO').find('PARTICIPACAO-EM-BANCA-DE-DOUTORADO') != None:
        for participation_board in root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO').findall('PARTICIPACAO-EM-BANCA-DE-DOUTORADO'):
          if 'Bancas de Doutorado' in self.board:
            self.board_quantity[self.board.index('Bancas de Doutorado')] += 1

          else:
            self.board.append('Bancas de Doutorado')
            self.board_quantity.append(1)

      if root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO').find('PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO') != None:
        for participation_board in root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO').findall('PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO'):
          if 'Bancas de Exame de Qualificação' in self.board:
            self.board_quantity[self.board.index('Bancas de Exame de Qualificação')] += 1

          else:
            self.board.append('Bancas de Exame de Qualificação')
            self.board_quantity.append(1)

      if root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO').find('PARTICIPACAO-EM-BANCA-DE-GRADUACAO') != None:
        for participation_board in root.find('DADOS-COMPLEMENTARES').find('PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO').findall('PARTICIPACAO-EM-BANCA-DE-GRADUACAO'):
          if 'Bancas de Graduação' in self.board:
            self.board_quantity[self.board.index('Bancas de Graduação')] += 1

          else:
            self.board.append('Bancas de Graduação')
            self.board_quantity.append(1)

    # Completed Orientations
    if root.find('OUTRA-PRODUCAO').find('ORIENTACOES-CONCLUIDAS') != None:
      if root.find('OUTRA-PRODUCAO').find('ORIENTACOES-CONCLUIDAS').find('ORIENTACOES-CONCLUIDAS-PARA-MESTRADO') != None:
          for orientation in root.find('OUTRA-PRODUCAO').find('ORIENTACOES-CONCLUIDAS').findall('ORIENTACOES-CONCLUIDAS-PARA-MESTRADO'):
            self.completed_orientations.append(orientation.find('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').attrib['ANO'])

      if root.find('OUTRA-PRODUCAO').find('ORIENTACOES-CONCLUIDAS').find('ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO') != None:
          for orientation in root.find('OUTRA-PRODUCAO').find('ORIENTACOES-CONCLUIDAS').findall('ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO'):
            self.completed_orientations.append(orientation.find('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').attrib['ANO'])

      if root.find('OUTRA-PRODUCAO').find('ORIENTACOES-CONCLUIDAS').find('OUTRAS-ORIENTACOES-CONCLUIDAS') != None:
          for orientation in root.find('OUTRA-PRODUCAO').find('ORIENTACOES-CONCLUIDAS').findall('OUTRAS-ORIENTACOES-CONCLUIDAS'):
            self.completed_orientations.append(orientation.find('DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS').attrib['ANO'])

    # In progress Orientations
    if root.find('DADOS-COMPLEMENTARES').find('ORIENTACOES-EM-ANDAMENTO') != None:
      if root.find('DADOS-COMPLEMENTARES').find('ORIENTACOES-EM-ANDAMENTO').find('ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO') != None:
        for orientation in root.find('DADOS-COMPLEMENTARES').find('ORIENTACOES-EM-ANDAMENTO').findall('ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO'):
          self.in_progress_orientations.append(orientation.find('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO').attrib['ANO'])

      if root.find('DADOS-COMPLEMENTARES').find('ORIENTACOES-EM-ANDAMENTO').find('ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO') != None:
        for orientation in root.find('DADOS-COMPLEMENTARES').find('ORIENTACOES-EM-ANDAMENTO').findall('ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO'):
          self.in_progress_orientations.append(orientation.find('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO').attrib['ANO'])

      if root.find('DADOS-COMPLEMENTARES').find('ORIENTACOES-EM-ANDAMENTO').find('ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA') != None:
        for orientation in root.find('DADOS-COMPLEMENTARES').find('ORIENTACOES-EM-ANDAMENTO').findall('ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA'):
          self.in_progress_orientations.append(orientation.find('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA').attrib['ANO'])