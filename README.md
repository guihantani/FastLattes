# FastLattes
Este projeto é referente a uma ferramenta em python para a extração de dados automatizada de currículos Lattes, e apresentação dos mesmos em um dashboard composto por gráficos

## 📋 Bibliotecas

O arquivo `requirements.txt` contém 5 bibliotecas externas do Python que são necessárias para rodar a ferramenta, são eles:

```
matplotlib==3.5.3
nltk==3.7
numpy==1.23.2
streamlit==1.12.2
wordcloud==1.8.2.2
```

## 🔧 Instalação

Primeiramente, deve ser necessário possuir alguma versão do Python 3. Após isso, é possível utilizar o `pip` para instalar as bibliotecas externas necessárias mencionadas anteriormente, o comando a ser utilizado no terminal é o seguinte:

```
pip install -r requirements.txt
```

Após isso, os arquivos zip dos currículos Lattes podem ser inseridos diretamente no diretório `lattes`, ou adicionados pelo módulo de upload de arquivos dentro da ferramenta.

Para rodar a ferramenta, é utilizado o seguinte comando da biblioteca `streamlit` no terminal:

```
streamlit run main.py
```

Assim que o comando for utilizado, é esperado que a aplicação abra no Browser padrão da máquina.