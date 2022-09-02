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
    st.pyplot(fig)
else:
    st.title(selectedPage)

