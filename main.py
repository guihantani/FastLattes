import os
import functions as functions
import streamlit as st

cur_path = os.path.dirname(__file__)
new_path = cur_path + '\lattes'

researchers = functions.initialize_researchers(new_path)
researchers_names = functions.extract_all_citations(researchers)
fig = functions.generate_works_per_year_graphic(researchers)

# Generate WebApp
researchers_names.insert(0, 'Dados Gerais')

st.sidebar.title('Menu')
selectedPage = st.sidebar.selectbox('Selecione a página', researchers_names)


if selectedPage == 'Dados Gerais':
    st.title('Dados Gerais')
    st.subheader('Trabalhos em Eventos')
    st.write('Total: ', len(functions.extract_all_works_years(researchers)))
    st.pyplot(fig)

else:
    st.title(selectedPage)
    for researcher in researchers:
        if researcher.name == selectedPage:
            st.write('ID ORCID: ', researcher.orcid)
            st.write('Endereço: ', researcher.address)
            st.write('Instituição: ', researcher.institution)
            st.text(' ')

            if researcher.works_years != []:
                st.subheader('Trabalhos em Eventos')
                st.write('Total: ', len(researcher.works_years))
                fig = functions.generate_works_per_year_graphic(researcher)
                st.pyplot(fig)
                st.text(' ')
                st.text(' ')

            if researcher.articles != []:
                st.subheader('Artigos')
                st.write('Total: ', len(researcher.articles))
                fig = functions.generate_articles_per_year_graphic(researcher)
                st.pyplot(fig)
                st.text(' ')
                st.text(' ')