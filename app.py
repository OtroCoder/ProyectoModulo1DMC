import streamlit as st

st.title("Proyecto módulo 1 Fundamentals")
st.sidebar.title("Parámetros")

st.image("Python.png")

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




'''
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Proyecto módulo 1 Fundamentals",
    page_icon="📊",
    layout="centered"
)

st.title("Proyecto módulo 1 Fundamentals")

st.sidebar.title("Parámetros")

opcion = st.sidebar.selectbox(
    "Selecciona un ejemplo",
    [
        "1. Presentación personal",
        "2. Calculadora de ventas",
        "3. Simulador de descuento",
        "4. Dashboard con tabla",
        "5. Dashboard con gráfico"
    ]
)

# --------------------------------------------------
# EJEMPLO 1: PRESENTACIÓN PERSONAL
# --------------------------------------------------

if opcion == "1. Presentación personal":

    st.header("Mi primera aplicación")

    nombre = st.sidebar.text_input("Escribe tu nombre")
    edad = st.sidebar.number_input(
        "Escribe tu edad",
        min_value=1,
        max_value=100,
        value=25
    )

    if nombre:
        st.write(f"Hola, {nombre}. Bienvenido a mi app en Streamlit.")
        st.write(f"Tienes {edad} años.")
    else:
        st.info("Escribe tu nombre en la barra lateral.")


# --------------------------------------------------
# EJEMPLO 2: CALCULADORA DE VENTAS
# --------------------------------------------------

elif opcion == "2. Calculadora de ventas":

    st.header("Calculadora simple de ventas")

    precio = st.sidebar.number_input(
        "Precio del producto",
        min_value=0.0,
        value=50.0
    )

    cantidad = st.sidebar.number_input(
        "Cantidad vendida",
        min_value=0,
        value=10
    )

    total = precio * cantidad

    st.write(f"Precio unitario: S/ {precio:.2f}")
    st.write(f"Cantidad vendida: {cantidad}")

    st.success(f"Venta total: S/ {total:.2f}")


# --------------------------------------------------
# EJEMPLO 3: SIMULADOR DE DESCUENTO
# --------------------------------------------------

elif opcion == "3. Simulador de descuento":

    st.header("Simulador de descuento")

    precio = st.sidebar.number_input(
        "Precio original",
        min_value=0.0,
        value=100.0
    )

    descuento = st.sidebar.slider(
        "Descuento (%)",
        min_value=0,
        max_value=100,
        value=10
    )

    monto_descuento = precio * descuento / 100
    precio_final = precio - monto_descuento

    st.write(f"Precio original: S/ {precio:.2f}")
    st.write(f"Descuento aplicado: {descuento}%")
    st.write(f"Monto descontado: S/ {monto_descuento:.2f}")

    st.success(f"Precio final: S/ {precio_final:.2f}")


# --------------------------------------------------
# EJEMPLO 4: DASHBOARD CON TABLA
# --------------------------------------------------

elif opcion == "4. Dashboard con tabla":

    st.header("Dashboard básico de ventas")

    datos = {
        "Producto": ["Laptop", "Polo", "Pan", "Mouse", "Casaca"],
        "Categoría": ["Tecnología", "Ropa", "Alimentos", "Tecnología", "Ropa"],
        "Ventas": [3500, 800, 300, 500, 1200]
    }

    df = pd.DataFrame(datos)

    categoria = st.sidebar.selectbox(
        "Selecciona una categoría",
        ["Todos", "Tecnología", "Ropa", "Alimentos"]
    )

    if categoria != "Todos":
        df = df[df["Categoría"] == categoria]

    st.dataframe(df)

    total_ventas = df["Ventas"].sum()

    st.metric("Total de ventas", f"S/ {total_ventas:.2f}")


# --------------------------------------------------
# EJEMPLO 5: DASHBOARD CON GRÁFICO
# --------------------------------------------------

elif opcion == "5. Dashboard con gráfico":

    st.header("Dashboard de ventas por producto")

    datos = {
        "Producto": ["Laptop", "Mouse", "Teclado", "Monitor", "Audífonos"],
        "Ventas": [3500, 500, 750, 1200, 950]
    }

    df = pd.DataFrame(datos)

    mostrar_tabla = st.sidebar.checkbox(
        "Mostrar tabla",
        value=True
    )

    st.subheader("Gráfico de barras")
    st.bar_chart(df.set_index("Producto"))

    total_ventas = df["Ventas"].sum()
    producto_mayor = df.loc[df["Ventas"].idxmax(), "Producto"]

    st.metric("Total de ventas", f"S/ {total_ventas:.2f}")
    st.metric("Producto con mayor venta", producto_mayor)

    if mostrar_tabla:
        st.subheader("Tabla de datos")
        st.dataframe(df)
'''
