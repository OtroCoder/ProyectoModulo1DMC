import streamlit as st

st.title("Proyecto módulo 1 Fundamentals")
st.sidebar.title("Parámetros")

st.image("python.png")
st.sidebar.image("dmc.png")

modulo=st.sidebar.selectbox("elija un módulo",["Modulo Listas","Modulo Array","Modulo Funciones"])

valor_inicial = st.number_input(
    "Ingrese el valor inicial",
    value=0
)

valor_final = st.number_input(
    "Ingrese el valor final",
    value=1
)

lista_numerica = list(range(valor_inicial, valor_final))

st.write(lista_numerica)





