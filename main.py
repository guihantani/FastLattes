import os
import functions as functions
import streamlit as st
from pathlib import Path
import nltk

cur_path = os.path.dirname(__file__)
new_path = cur_path + '\lattes'
nltk.download('stopwords')

researchers = functions.initialize_researchers(new_path)
researchers_names = functions.extract_all_citations(researchers)

# Generate WebApp
researchers_names.insert(0, 'Dados Gerais')

st.sidebar.title('Menu')
selectedPage = st.sidebar.selectbox('Selecione a página', researchers_names)
min_year = st.sidebar.number_input(label='Ano Mínimo (Inserir 0 para resetar)', step = 1, format = "%i")
max_year = st.sidebar.number_input(label='Ano Máximo (Inserir 0 para resetar)', step = 1, format = "%i")
st.sidebar.text(' ')
st.sidebar.text(' ')
generate_word_cloud = st.sidebar.checkbox('Gerar Nuvem de Palavras (Torna o programa mais lento)')
st.sidebar.text(' ')
st.sidebar.text(' ')
Files = st.sidebar.file_uploader(label = "Adicione Múltiplos Lattes (Tipo Zip)", type=["zip"], accept_multiple_files=True)

if Files:
    for File in Files:
        save_folder = os.path.realpath(__file__)[:-7] + 'lattes'
        save_path = Path(save_folder, File.name)
        with open(save_path, mode='wb') as w:
            w.write(File.getvalue())
        if save_path.exists():
            st.success(f'Arquivo {File.name} foi salvo com sucesso! (Atualize a página)')
    Files = None


if selectedPage == 'Dados Gerais':
    st.title('Dados Gerais')
    if researchers != [] and generate_word_cloud == True:
        st.header('Nuvem de Palavras')
        with st.spinner('Gerando a Nuvem de Palavras, por favor aguarde...'):
            st.pyplot(functions.generate_word_cloud(researchers))
        st.header(' ')

    works_per_years_result = functions.generate_works_per_year_graphic(researchers, min_year, max_year)
    if works_per_years_result != None:
        st.header('Trabalhos em Eventos')
        st.write('Total: ', works_per_years_result[1])
        works_per_years_graphic = works_per_years_result[0]
        st.pyplot(works_per_years_graphic)
        st.header(' ')

    articles_years_graphic = functions.generate_articles_per_year_graphic(researchers, min_year, max_year)
    if articles_years_graphic != None:
        st.header('Artigos')
        st.write('Total: ', len(functions.extract_all_articles_years(researchers)))
        st.pyplot(articles_years_graphic)
        st.header(' ')

    boards_piechart, board_quantities = functions.generate_boards_piechart(researchers, min_year, max_year)
    if boards_piechart != None:
        st.header('Participações em Bancas')
        st.write('Total: ', sum(board_quantities))
        st.pyplot(boards_piechart)
        st.header(' ')

    completed_orientations_graphic = functions.generate_completed_orientations_per_year_graphic(researchers, min_year, max_year)
    in_progress_orientations_graphic = functions.generate_in_progress_orientations_per_year_graphic(researchers,min_year, max_year)
    if completed_orientations_graphic != None or in_progress_orientations_graphic != None:
        st.header('Orientações')
        if completed_orientations_graphic != None:
            st.subheader('Orientações Completas')
            st.write('Total: ', len(functions.extract_all_completed_orientation_years(researchers)))
            st.pyplot(completed_orientations_graphic)
            st.text(' ')

        if in_progress_orientations_graphic != None:
            st.subheader('Orientações Em Progresso')
            st.write('Total: ', len(functions.extract_all_in_progress_orientation_years(researchers)))
            st.pyplot(in_progress_orientations_graphic)
            st.header(' ')

        projects_piechart, project_quantities = functions.generate_projects_piechart(researchers, min_year, max_year)
        if projects_piechart != None:
            st.header('Participações em Projetos')
            st.write('Total: ', sum(project_quantities))
            st.pyplot(projects_piechart)
            st.header(' ')


else:
    st.title(selectedPage)
    for researcher in researchers:
        if researcher.name == selectedPage:
            st.write('ID ORCID: ', researcher.orcid)
            st.write('Endereço: ', researcher.address)
            st.write('Instituição: ', researcher.institution)
            if st.button('Deletar Pesquisador'):
                functions.delete_researcher_file(researcher, new_path)
                st.experimental_rerun()
            st.text(' ')

            if researcher.words != None and generate_word_cloud == True:
                st.header('Nuvem de Palavras')
                with st.spinner('Gerando a Nuvem de Palavras, por favor aguarde...'):
                    st.pyplot(functions.generate_word_cloud(researcher))
                st.header(' ')

            researcher_works_per_years_result = functions.generate_works_per_year_graphic(researcher, min_year, max_year)
            if researcher_works_per_years_result != None:
                st.header('Trabalhos em Eventos')
                st.write('Total: ', researcher_works_per_years_result[1])
                works_per_years_graphic = researcher_works_per_years_result[0]
                st.pyplot(works_per_years_graphic)
                st.header(' ')

            researcher_articles_years_graphic = functions.generate_articles_per_year_graphic(researcher, min_year, max_year)
            if researcher_articles_years_graphic != None:
                st.header('Artigos')
                st.write('Total: ', len(researcher.articles))
                st.pyplot(researcher_articles_years_graphic)
                st.header(' ')

            researcher_boards_piechart, researcher_board_quantities = functions.generate_boards_piechart(researcher, min_year, max_year)
            if researcher_boards_piechart != None:
                st.header('Participações em Bancas')
                st.write('Total: ', sum(researcher_board_quantities))
                st.pyplot(researcher_boards_piechart)
                st.header(' ')

            researcher_completed_orientations_graphic = functions.generate_completed_orientations_per_year_graphic(researcher, min_year, max_year)
            researcher_in_progress_orientations_graphic = functions.generate_in_progress_orientations_per_year_graphic(researcher, min_year, max_year)
            if researcher_completed_orientations_graphic != None or researcher_in_progress_orientations_graphic != None:
                st.header('Orientações')
                if researcher_completed_orientations_graphic != None:
                    st.subheader('Orientações Completas')
                    st.write('Total: ', len(functions.extract_all_completed_orientation_years(researcher)))
                    st.pyplot(researcher_completed_orientations_graphic)
                    st.text(' ')
                if researcher_in_progress_orientations_graphic != None:
                    st.subheader('Orientações Em Progresso')
                    st.write('Total: ', len(functions.extract_all_in_progress_orientation_years(researcher)))
                    st.pyplot(researcher_in_progress_orientations_graphic)
                    st.header(' ')

            researcher_projects_piechart, researcher_project_quantities = functions.generate_projects_piechart(researcher, min_year,max_year)
            if researcher_projects_piechart != None:
                st.header('Participações em Projetos')
                st.write('Total: ', sum(researcher_project_quantities))
                st.pyplot(researcher_projects_piechart)
                st.header(' ')
