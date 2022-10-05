import os
import functions as functions
import streamlit as st
import numpy as np

cur_path = os.path.dirname(__file__)
new_path = cur_path + '\lattes'

researchers = functions.initialize_researchers(new_path)
researchers_names = functions.extract_all_citations(researchers)

# Generate WebApp
researchers_names.insert(0, 'Dados Gerais')

st.sidebar.title('Menu')
selectedPage = st.sidebar.selectbox('Selecione a página', researchers_names)
min_year = st.sidebar.number_input(label='Ano Mínimo', step = 1, format = "%i")
max_year = st.sidebar.number_input(label='Ano Máximo', step = 1, format = "%i")


if selectedPage == 'Dados Gerais':
    st.title('Dados Gerais')
    st.header('Trabalhos em Eventos')
    works_per_years_result = functions.generate_works_per_year_graphic(researchers, min_year, max_year)
    st.write('Total: ', works_per_years_result[1])
    works_per_years_graphic = works_per_years_result[0]
    st.pyplot(works_per_years_graphic)
    st.text(' ')
    st.text(' ')

    st.header('Artigos')
    st.write('Total: ', len(functions.extract_all_articles_years(researchers)))
    articles_years_graphic = functions.generate_articles_per_year_graphic(researchers)
    st.pyplot(articles_years_graphic)
    st.text(' ')
    st.text(' ')

    boards_piechart, board_quantities = functions.generate_boards_piechart(researchers, min_year, max_year)
    if boards_piechart != None:
        st.header('Participações em Bancas')
        st.write('Total: ', sum(board_quantities))
        st.pyplot(boards_piechart)

    st.header('Orientações')
    st.subheader('Orientações Completas')
    st.write('Total: ', len(functions.extract_all_completed_orientation_years(researchers)))
    completed_orientations_graphic = functions.generate_completed_orientations_per_year_graphic(researchers)
    st.pyplot(completed_orientations_graphic)
    st.text(' ')
    st.subheader('Orientações Em Progresso')
    st.write('Total: ', len(functions.extract_all_in_progress_orientation_years(researchers)))
    in_progress_orientations_graphic = functions.generate_in_progress_orientations_per_year_graphic(researchers)
    st.pyplot(in_progress_orientations_graphic)
    st.text(' ')
    st.text(' ')

else:
    st.title(selectedPage)
    for researcher in researchers:
        if researcher.name == selectedPage:
            st.write('ID ORCID: ', researcher.orcid)
            st.write('Endereço: ', researcher.address)
            st.write('Instituição: ', researcher.institution)
            st.text(' ')

            if researcher.works_years != []:
                st.header('Trabalhos em Eventos')
                works_per_years_result = functions.generate_works_per_year_graphic(researcher, min_year, max_year)
                st.write('Total: ', works_per_years_result[1])
                works_per_years_graphic = works_per_years_result[0]
                st.pyplot(works_per_years_graphic)
                st.text(' ')
                st.text(' ')

            if researcher.articles != []:
                st.header('Artigos')
                st.write('Total: ', len(researcher.articles))
                articles_years_graphic = functions.generate_articles_per_year_graphic(researcher)
                st.pyplot(articles_years_graphic)
                st.text(' ')
                st.text(' ')

            if researcher.board != []:
                boards_piechart, board_quantities = functions.generate_boards_piechart(researcher, min_year, max_year)
                if boards_piechart != None:
                    st.header('Participações em Bancas')
                    st.write('Total: ', sum(board_quantities))
                    st.pyplot(boards_piechart)
                    st.text(' ')
                    st.text(' ')

            if researcher.completed_orientations or researcher.in_progress_orientations != []:
                st.header('Orientações')
                if researcher.completed_orientations != []:
                    st.subheader('Orientações Completas')
                    st.write('Total: ', len(functions.extract_all_completed_orientation_years(researcher)))
                    completed_orientations_graphic = functions.generate_completed_orientations_per_year_graphic(researcher)
                    st.pyplot(completed_orientations_graphic)
                    st.text(' ')
                if researcher.in_progress_orientations != []:
                    st.subheader('Orientações Em Progresso')
                    st.write('Total: ', len(functions.extract_all_in_progress_orientation_years(researchers)))
                    in_progress_orientations_graphic = functions.generate_in_progress_orientations_per_year_graphic(researchers)
                    st.pyplot(in_progress_orientations_graphic)
                    st.text(' ')
                    st.text(' ')