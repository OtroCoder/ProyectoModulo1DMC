import streamlit as st
import numpy as np
import libreria_funciones as lf

st.title("Proyecto módulo 1 Fundamentals")
st.sidebar.title("Parámetros")

st.image("python.png")
st.sidebar.image("dmc.png")

modulo = st.sidebar.selectbox(
    "Elija un módulo",
    ["Modulo Listas", "Modulo Array", "Modulo Funciones"]
)

if modulo == "Modulo Listas":

    valor_inicial = st.number_input(
        "Ingrese el valor inicial",
        value=0,
        step=1
    )

    valor_final = st.number_input(
        "Ingrese el valor final",
        value=1,
        step=1
    )

    lista_numerica = list(range(valor_inicial, valor_final))

    st.write("Lista generada:", lista_numerica)

elif modulo == "Modulo Array":

    st.write("Estás en el módulo de arreglos")

    limite_inferior = st.number_input(
        "Ingrese el límite inferior",
        value=1200,
        step=1
    )

    limite_superior = st.number_input(
        "Ingrese el límite superior",
        value=1250,
        step=1
    )

    cantidad_datos = st.number_input(
        "Ingrese la cantidad de datos a crear",
        value=31,
        min_value=1,
        step=1
    )

    datos_produccion = np.random.randint(
        limite_inferior,
        limite_superior,
        size=cantidad_datos
    )

    st.write("Datos de producción:", datos_produccion)
    st.write("La producción total es:", np.sum(datos_produccion))
    st.write("La producción promedio es:", np.mean(datos_produccion))

else:

    st.write("Estás en el módulo de funciones")
    principal = st.number_input("Ingrese el Monto del prestamo", value=0, step=1  )
    tasa_anual=st.number_input("Ingrese la tasa anual en decimal", value=0, step=1  )
    anios    =st.number_input("Ingrese el numero de años del presamo", value=1, step=1  )
    pagos_por_anio=st.number_input("Ingrese pago por anios", value=12, step=1  )

    cuota=lf.cuota_prestamo(principal, tasa_anual, anios, pagos_por_anio)
    st.write("La cuota Mensual de prestamo será",cuota)
