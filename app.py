import streamlit as st
import numpy as np

st.title("Proyecto módulo 1 Fundamentals")
st.sidebar.title("Parámetros")

st.image("python.png")
st.sidebar.image("dmc.png")

modulo=st.sidebar.selectbox("elija un módulo",["Modulo Listas","Modulo Array","Modulo Funciones"])

if modulo=="Modulo Listas":
    
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

elif modulo=="Modulo Array":
    st.write("Estas en el módulo de arreglos")

    limite_inferior = st.number_input(
        "Ingrese el límite inferior",
        value=1200
    )

    limite_superior = st.number_input(
        "Ingrese el límite superior",
        value=1250
    )

    cantidad_datos = st.number_input(
        "Ingrese totalidad de datos a crear",
        value=31
    )

    datos_produccion = np.random.randint()
     st.write(datos_produccion)
     st.write("La producción total es:" ,  np.sum(datos_produccion))
     st.write("La producción promedio es:" , np.mean(datos_produccion) )


else:
    st.write("Estas en el módulo de funciones")





