import streamlit as st

st.title("Proyecto módulo 1 Fundamentals")

st.sidebar.title("Parámetros")

nombre = st.sidebar.text_input("Escribe tu nombre")
edad = st.sidebar.number_input("Escribe tu edad", min_value=1, max_value=100)

st.header("Mi primera aplicación")

if nombre:
    st.write(f"Hola, {nombre}. Bienvenido a mi app en Streamlit.")
    st.write(f"Tienes {edad} años.")
else:
    st.write("Escribe tu nombre en la barra lateral.")
