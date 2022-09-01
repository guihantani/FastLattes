import os
import functions as functions
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

cur_path = os.path.dirname(__file__)
new_path = cur_path + '\lattes'

print(functions.extract_all_citations(new_path))

# Make works per year graphic
y = np.array(functions.extract_all_works_years(new_path))
y.sort()

unique_y = []
y_count = []

for x in y:
    if x not in unique_y:
        unique_y.append(x)
        y_count.append(0)

for x in y:
    index = unique_y.index(x)
    y_count[index] += 1

fig, ax = plt.subplots(figsize=(len(unique_y), max(y_count) - 3))
ax.bar(unique_y, y_count, edgecolor = "black")
for i in range(len(unique_y)):
    ax.text(i, y_count[i], y_count[i], ha = "center")

plt.xlabel('Anos')
plt.ylabel('Número de Trabalhos')

st.title('Dados gerais do Lattes')
st.sidebar.title('Menu')
st.pyplot(fig)