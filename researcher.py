class Researcher:
  def __init__(self, root):
    self.name = root[0].attrib['NOME-COMPLETO']
    self.works_years = []

    if len(root[1]) != 0:
      for child in root[1][0]:
        self.works_years.append(child[0].attrib['ANO-DO-TRABALHO'])

