# =============================================================================
# PROYECTO 1 - APLICACIÓN EN STREAMLIT
# Especialización Python for Analytics | Módulo 1 - Python Fundamentals
# Autor: Otto Morales Gómez
# Año: 2026
# -----------------------------------------------------------------------------
# Esta aplicación integra los conceptos fundamentales del módulo:
# variables, estructuras de datos, control de flujo, funciones,
# programación funcional y programación orientada a objetos (POO).
#
# Características de robustez incorporadas en esta versión:
#   - Manejo controlado de excepciones (ValueError, ZeroDivisionError, Exception)
#   - Validación y saneamiento de entradas de texto (longitud, caracteres)
#   - Tooltips de ayuda (parámetro help=) en todos los campos
#   - Formato monetario peruano es_PE: S/ 1,500.75 (Ley N.º 30381: símbolo "S/")
#   - Identidad visual con paleta corporativa y logo embebido (sin depender
#     de internet ni de archivos externos)
#
# Para ejecutarla localmente:
#     streamlit run app.py
# =============================================================================

# --- Importación de librerías base ---
# streamlit : framework para construir la interfaz web interactiva
# pandas    : manejo de tablas de datos (DataFrame)
# numpy     : manejo de arreglos numéricos (arrays)
import base64
import html

import streamlit as st
import pandas as pd
import numpy as np

# =============================================================================
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# (debe ser la primera llamada a Streamlit del script)
# =============================================================================
st.set_page_config(
    page_title="Proyecto 1 - Otto Morales",
    page_icon="💡",
    layout="wide"
)

# =============================================================================
# IMPORTACIÓN SEGURA DE LAS LIBRERÍAS EXTERNAS DEL PROYECTO
# -----------------------------------------------------------------------------
# Si alguno de los archivos del curso no está junto a app.py, la aplicación
# se detiene con un mensaje claro en lugar de mostrar un traceback crudo.
# =============================================================================
try:
    from libreria_funciones_proyecto1 import calcular_cuota_prestamo_frances
    from libreria_clases_proyecto1 import ProyectoInversion
except ImportError as error_importacion:
    st.error(
        "🚫 **No se pudieron cargar las librerías del proyecto.** "
        "Verifica que `libreria_funciones_proyecto1.py` y "
        "`libreria_clases_proyecto1.py` estén en la misma carpeta que `app.py`. "
        f"\n\nDetalle técnico: `{error_importacion}`"
    )
    st.stop()

# =============================================================================
# CONSTANTES DE LA APLICACIÓN
# =============================================================================
PALETA = {
    "fondo": "#fbfbfb",       # gris casi blanco (fondo general)
    "turquesa": "#0ad9d8",    # acento positivo / métricas
    "naranja_oscuro": "#cf480e",
    "naranja": "#f17507",     # color principal de marca
    "navy": "#092c4d",        # azul marino (textos y sidebar)
}

MAX_CARACTERES_TEXTO = 60          # longitud máxima de conceptos y nombres
MAX_REGISTROS_HISTORICO = 100      # tope del histórico del E3 (evita crecer sin fin)
MAX_MONTO = 1_000_000_000_000.0    # tope de montos (1 billón de soles)

# Logo corporativo embebido en base64 (autocontenido: no requiere internet
# ni archivos externos para renderizar la identidad visual).
LOGO_BASE64 = "iVBORw0KGgoAAAANSUhEUgAABDgAAAQ4CAMAAADbzpy9AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAKJQTFRFzkgN+9zC+LmG9ZZK8nwc/vbw9qho/OXR+sqk84Ur/e3h9I0797B3+cKV+9Oz9Z9Z5qOG2nZK0VMc9t3R/PTw+ejh11MN4I1o6GgN89HC4F4N12o71F8r7bqk6a+V3YFZ8Maz5Jh35GMN73AN1VAN6msN0EsN7W4N3VsN5mYN0k0N21gN4mAN2VUN8rqV4W8r5IpZ5oxZ2Fwc34RZ8XMN////ucFbVQAAADZ0Uk5T//////////////////////////////////////////////////////////////////////8AoY9OMQAALNdJREFUeNrs3eli20aCqFFhIbiTkm1tluUla3cnPXeD3//VrmQ7iSlLtggUUAXgnF/TMz1xLEAfawN48hHgSCd+BIBwAMIBCAcgHIBwAAgHIByAcADCAQgHgHAAwgEIByAcgHAACAcgHIBwAMIBCAcgHADCAQgHIByAcADCASAcgHAAwgEIByAcAMIBCAcgHIBwAMIBIByAcADCAQgHIByAcAAIByAcgHAAwgEIB4BwAMIBCAcgHIBwAAgHIByAcADCAQgHgHAAwgEIByAcgHAAwgEgHIBwAMIBCAcgHADCAQgHIByAcADCASAcgHAAwgEIByAcAMIBCAcgHIBwAMIBCAeAcADCAQgHIByAcAAIByAcgHAAwgEIB4BwAMIBCAcgHIBwAMIBIByAcADCAQgHIBwAwgEIByAcgHAAwgEgHIBwAMIBCAcgHADCAQgHIByAcADCAQgHgHAAwgEIByAcgHAACAcgHIBwAMIBCAeAcADCAQgHIByAcAAIByAcgHAAwgEIByAcAMIBCAcgHIBwAMIBIByAcADCAQgHIBwAwgEIByAcgHAAwgEgHIBwAMIBCAcgHIBwAAgHIByAcADCAQgHgHAAwgEIByAcgHAACAcgHIBwAMIBCAcgHADCAQgHPVpld/LPquIvX/4Xi/v/o58RwsG9LFvk+V0f6mdaFsUmz7Ns5kcnHEzPPMs3z8/F4wmp7sYhAiIcTMEs226KZR3OXT+yuZ+rcDDaacliU5R1N4pqa/QhHIytGdtqXXduuc8toAoHo7Da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"


# =============================================================================
# FUNCIONES UTILITARIAS (formato es_PE, saneamiento y estilos)
# =============================================================================
def formatear_moneda(valor: float) -> str:
    """
    Formatea un monto según la convención oficial peruana (locale es_PE):
    separador de miles con coma y decimal con punto -> S/ 1,500.75
    El símbolo oficial del sol es "S/" (Ley N.º 30381, año 2015).
    """
    try:
        return f"S/ {float(valor):,.2f}"
    except (TypeError, ValueError):
        return "S/ —"


def formatear_numero(valor: float, decimales: int = 2) -> str:
    """Formatea un número genérico con miles (,) y decimales (.) según es_PE."""
    try:
        return f"{float(valor):,.{decimales}f}"
    except (TypeError, ValueError):
        return "—"


def limpiar_texto(texto: str) -> str:
    """
    Sanea una entrada de texto del usuario:
    - recorta espacios en los extremos y colapsa espacios múltiples
    - escapa caracteres HTML y neutraliza símbolos de Markdown,
      evitando inyección de formato en los mensajes de la interfaz
    """
    limpio = " ".join(str(texto).split())
    limpio = html.escape(limpio)
    for simbolo in ("*", "_", "`", "#", "[", "]", ">"):
        limpio = limpio.replace(simbolo, "")
    return limpio.strip()


# =============================================================================
# VALORES POR DEFECTO DE LOS FORMULARIOS
# -----------------------------------------------------------------------------
# Cada campo de entrada tiene una clave (key) registrada en st.session_state.
# Este diccionario define su valor inicial y, sobre todo, el valor al que
# vuelve el campo despues de un registro exitoso: asi el formulario queda
# limpio y listo para el siguiente ingreso.
# =============================================================================
MAX_ANIOS_FLUJOS = 10          # horizonte maximo de flujos en el Ejercicio 4
VALOR_FLUJO_INICIAL = 40000.0  # flujo anual sugerido por defecto

VALORES_FORMULARIO = {
    # --- Ejercicio 1: flujo de caja ---
    "e1_concepto": "",
    "e1_tipo": "Ingreso",
    "e1_valor": 0.0,
    # --- Ejercicio 2: registro de productos con NumPy ---
    "e2_nombre": "",
    "e2_categoria": "Tecnología",
    "e2_precio": 0.0,
    "e2_cantidad": 1,
    # --- Ejercicio 3: parametros del prestamo (sistema frances) ---
    "e3_monto": 50000.0,
    "e3_tasa": 18.0,
    "e3_plazo": 24,
    # --- Ejercicio 4: creacion de proyectos de inversion ---
    "e4_nombre": "",
    "e4_inversion": 100000.0,
    "e4_tasa": 12.0,
    "e4_anios": 3,
}

# Los flujos anuales del Ejercicio 4 son dinamicos: se prepara una clave por año
for _anio in range(MAX_ANIOS_FLUJOS):
    VALORES_FORMULARIO[f"flujo_{_anio}"] = VALOR_FLUJO_INICIAL


# Sección a la que pertenece cada campo, según el prefijo de su clave
SECCION_DEL_PREFIJO = {
    "e1_": "Ejercicio 1",
    "e2_": "Ejercicio 2",
    "e3_": "Ejercicio 3",
    "e4_": "Ejercicio 4",
    "flujo_": "Ejercicio 4",
}


def seccion_del_campo(clave: str) -> str:
    """Devuelve el ejercicio al que pertenece un campo del formulario."""
    for prefijo, seccion in SECCION_DEL_PREFIJO.items():
        if clave.startswith(prefijo):
            return seccion
    return ""


def sincronizar_formularios() -> None:
    """
    Inicializa y PRESERVA el contenido de los formularios entre secciones.

    Streamlit descarta de session_state la clave de todo widget que no se
    dibuja en una corrida: al pasar de E1 a E2, lo escrito en E1 se perderia.
    Para evitarlo, cada campo tiene una clave espejo (con guion bajo delante)
    que no pertenece a ningun widget y por lo tanto sobrevive.

    El criterio es la seccion que estuvo visible en la corrida anterior
    (`seccion_previa`), porque solo esos campos traen datos vigentes del
    navegador:

      - campos de la seccion previa -> se respaldan en su espejo
      - los demas                   -> se restituyen desde su espejo

    Debe ejecutarse al inicio del script, antes de dibujar cualquier widget.
    """
    seccion_previa = st.session_state.get("seccion_previa", "")

    for clave, valor_inicial in VALORES_FORMULARIO.items():
        espejo = f"_{clave}"
        if seccion_del_campo(clave) == seccion_previa and clave in st.session_state:
            st.session_state[espejo] = st.session_state[clave]
        else:
            st.session_state[clave] = st.session_state.get(espejo, valor_inicial)


def registrar_cambio_de_seccion(seccion_actual: str) -> None:
    """
    Deja constancia de la seccion visible y, cuando el usuario cambia de
    ejercicio, desactiva las confirmaciones de borrado que hayan quedado
    abiertas, para no regresar a una advertencia a medio camino.
    """
    if st.session_state.get("seccion_previa") != seccion_actual:
        for clave in list(st.session_state.keys()):
            if str(clave).startswith("confirmar_"):
                st.session_state[clave] = False
    st.session_state.seccion_previa = seccion_actual


def reiniciar_campos(*prefijos: str) -> None:
    """
    Devuelve a su valor inicial todos los campos cuya clave empieza con
    alguno de los prefijos indicados.

    Solo debe invocarse desde un callback (parametro on_click del boton).
    Streamlit ejecuta los callbacks ANTES de volver a dibujar los widgets,
    por lo que en ese momento si esta permitido reasignar en session_state
    la clave de un widget; hacerlo despues de dibujarlo lanza excepcion.
    """
    for clave, valor in VALORES_FORMULARIO.items():
        if clave.startswith(prefijos):
            st.session_state[clave] = valor


def apilar_mensaje(clave: str, tipo: str, texto: str) -> None:
    """Guarda un mensaje generado dentro de un callback para mostrarlo luego."""
    st.session_state.setdefault(clave, []).append((tipo, texto))


def mostrar_mensajes(clave: str) -> None:
    """Muestra (y consume) los mensajes pendientes de un formulario."""
    despachador = {"ok": st.success, "error": st.error, "aviso": st.warning}
    for tipo, texto in st.session_state.pop(clave, []):
        despachador.get(tipo, st.info)(texto)


def boton_limpiar_confirmado(etiqueta: str, clave: str, accion,
                             advertencia: str) -> None:
    """
    Boton destructivo en dos pasos.

    El primer clic no borra nada: activa una bandera en session_state que
    despliega la advertencia junto a los botones de confirmar o cancelar.
    Solo el boton de confirmacion ejecuta la funcion `accion`.
    """
    bandera = f"confirmar_{clave}"

    if not st.session_state.get(bandera, False):
        if st.button(etiqueta, key=f"btn_{clave}"):
            st.session_state[bandera] = True
            st.rerun()
        return

    st.warning(advertencia)
    col_si, col_no, _ = st.columns([1, 1, 3])
    with col_si:
        if st.button("✅ Sí, eliminar", key=f"si_{clave}"):
            accion()
            st.session_state[bandera] = False
            st.rerun()
    with col_no:
        if st.button("↩️ Cancelar", key=f"no_{clave}"):
            st.session_state[bandera] = False
            st.rerun()


def mostrar_logo(ancho: int = 220) -> None:
    """Muestra el logo corporativo embebido (base64) con el ancho indicado."""
    try:
        st.image(base64.b64decode(LOGO_BASE64), width=ancho)
    except Exception:
        # Si por alguna razón el logo no decodifica, la app sigue funcionando.
        st.markdown("### 💡")


def encabezado_hero(chip: str, titulo: str, subtitulo: str) -> None:
    """
    Dibuja un encabezado tipo banner moderno (hero) con el logo discreto,
    una etiqueta superior (chip), el título y un subtítulo.
    """
    st.markdown(
        f"""
        <div class="hero">
          <img src="data:image/png;base64,{LOGO_BASE64}" alt="logo"/>
          <div>
            <span class="hero-chip">{chip}</span>
            <div class="hero-titulo">{titulo}</div>
            <p class="hero-sub">{subtitulo}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def inyectar_estilos() -> None:
    """
    Inyecta el CSS de identidad visual (HTML moderno dentro de app.py):
    paleta corporativa, tarjetas con sombra suave, botones con degradado
    y sidebar en azul marino.
    """
    st.markdown(
        f"""
        <style>
        /* ---------- Fondo general y tipografía ---------- */
        .stApp {{
            background-color: {PALETA['fondo']};
        }}
        h1, h2, h3 {{
            color: {PALETA['navy']} !important;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}

        /* ---------- Sidebar en azul marino ---------- */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PALETA['navy']} 0%, #0d3a63 100%);
        }}
        [data-testid="stSidebar"] * {{
            color: #ffffff !important;
        }}

        /* ---------- Marca discreta en el sidebar ---------- */
        .marca-sidebar {{
            display: flex; align-items: center; gap: 12px;
            padding: 6px 2px 14px 2px;
            border-bottom: 1px solid rgba(255,255,255,.14);
            margin-bottom: 14px;
        }}
        .marca-sidebar img {{
            height: 44px; width: 44px;
            background: #ffffff; border-radius: 12px; padding: 5px;
        }}
        .marca-nombre {{ font-weight: 700; font-size: 1.05rem; }}
        .marca-sub {{ font-size: .78rem; opacity: .75; }}

        /* ---------- Navegación tipo píldoras (st.radio) ---------- */
        [data-testid="stSidebar"] [role="radiogroup"] > label {{
            background: rgba(255,255,255,.07);
            border: 1px solid rgba(255,255,255,.14);
            border-radius: 12px;
            padding: 10px 14px;
            margin-bottom: 8px;
            width: 100%;
            transition: background .15s ease, transform .1s ease;
            cursor: pointer;
        }}
        [data-testid="stSidebar"] [role="radiogroup"] > label:hover {{
            background: rgba(255,255,255,.18);
            transform: translateX(2px);
        }}
        [data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {{
            background: linear-gradient(90deg, {PALETA['naranja']} 0%, {PALETA['naranja_oscuro']} 100%);
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(241, 117, 7, .40);
        }}
        /* Oculta el círculo del radio para que parezca un menú */
        [data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child {{
            display: none;
        }}

        /* ---------- Encabezado hero (estilo banner moderno) ---------- */
        .hero {{
            background: linear-gradient(120deg, {PALETA['navy']} 0%, #0d3a63 55%, #11507f 100%);
            border-radius: 18px;
            padding: 26px 32px;
            margin-bottom: 10px;
            display: flex; align-items: center; gap: 20px;
            box-shadow: 0 10px 28px rgba(9, 44, 77, .28);
        }}
        .hero img {{
            height: 58px; width: 58px;
            background: #ffffff; border-radius: 14px; padding: 7px;
            flex-shrink: 0;
        }}
        .hero .hero-titulo {{
            color: #ffffff; font-size: 1.65rem; font-weight: 800;
            margin: 0; letter-spacing: -0.02em; line-height: 1.2;
        }}
        .hero .hero-sub {{
            color: #b9d4ea; margin: 5px 0 0 0; font-size: .95rem;
        }}
        .hero .hero-chip {{
            display: inline-block;
            background: rgba(10, 217, 216, .16);
            color: {PALETA['turquesa']};
            border: 1px solid rgba(10, 217, 216, .35);
            border-radius: 999px;
            padding: 3px 12px;
            font-size: .74rem; font-weight: 700;
            letter-spacing: .06em; text-transform: uppercase;
            margin-bottom: 8px;
        }}

        /* ---------- Botones: degradado naranja de marca ---------- */
        .stButton > button {{
            background: linear-gradient(90deg, {PALETA['naranja']} 0%, {PALETA['naranja_oscuro']} 100%);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 0.55rem 1.2rem;
            font-weight: 600;
            transition: transform .12s ease, box-shadow .12s ease;
            box-shadow: 0 2px 8px rgba(241, 117, 7, 0.35);
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(207, 72, 14, 0.45);
            color: #ffffff;
        }}

        /* ---------- Métricas como tarjetas ---------- */
        [data-testid="stMetric"] {{
            background: #ffffff;
            border: 1px solid #eceff3;
            border-left: 5px solid {PALETA['turquesa']};
            border-radius: 12px;
            padding: 14px 18px;
            box-shadow: 0 2px 10px rgba(9, 44, 77, 0.06);
        }}
        [data-testid="stMetricLabel"] {{
            color: {PALETA['navy']};
            font-weight: 600;
        }}
        [data-testid="stMetricValue"] {{
            color: {PALETA['navy']};
        }}

        /* ---------- Pestañas (CRUD) ---------- */
        .stTabs [data-baseweb="tab"] {{
            font-weight: 600;
            color: {PALETA['navy']};
        }}
        .stTabs [aria-selected="true"] {{
            color: {PALETA['naranja_oscuro']} !important;
            border-bottom-color: {PALETA['naranja']} !important;
        }}

        /* ---------- Tarjeta de presentación (Home) ---------- */
        .tarjeta-home {{
            background: #ffffff;
            border: 1px solid #eceff3;
            border-radius: 16px;
            padding: 26px 30px;
            box-shadow: 0 4px 18px rgba(9, 44, 77, 0.08);
        }}
        .tarjeta-home table {{ width: 100%; border-collapse: collapse; }}
        .tarjeta-home td {{
            padding: 7px 4px;
            border-bottom: 1px solid #f0f2f5;
            color: {PALETA['navy']};
        }}
        .tarjeta-home td.campo {{ font-weight: 700; width: 34%; }}
        .banda-marca {{
            height: 6px;
            border-radius: 6px;
            margin: 6px 0 18px 0;
            background: linear-gradient(90deg,
                {PALETA['navy']} 0%, {PALETA['turquesa']} 35%,
                {PALETA['naranja']} 70%, {PALETA['naranja_oscuro']} 100%);
        }}
        .pie-pagina {{
            text-align: center;
            color: {PALETA['navy']};
            opacity: .65;
            font-size: .85rem;
            margin-top: 30px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# INICIALIZACIÓN DEL ESTADO DE LA SESIÓN (st.session_state)
# -----------------------------------------------------------------------------
# Streamlit vuelve a ejecutar todo el script con cada interacción; los datos
# se preservan entre interacciones guardándolos en st.session_state.
# =============================================================================

# Ejercicio 1: lista de movimientos del flujo de caja
if "movimientos" not in st.session_state:
    st.session_state.movimientos = []

# Ejercicio 2: arrays de NumPy (uno por cada campo del registro de productos)
if "arr_productos" not in st.session_state:
    st.session_state.arr_productos = np.array([], dtype=object)   # nombres
    st.session_state.arr_categorias = np.array([], dtype=object)  # categorías
    st.session_state.arr_precios = np.array([], dtype=float)      # precios
    st.session_state.arr_cantidades = np.array([], dtype=int)     # cantidades
    st.session_state.arr_totales = np.array([], dtype=float)      # totales

# Ejercicio 3: histórico de resultados de la función de préstamo francés
if "historico_prestamo" not in st.session_state:
    st.session_state.historico_prestamo = []

# Ejercicio 4: diccionario {nombre_proyecto: objeto ProyectoInversion}
if "proyectos" not in st.session_state:
    st.session_state.proyectos = {}

# Campos de los formularios: se restituye lo escrito en otras secciones
sincronizar_formularios()

# Los estilos se inyectan una sola vez por ejecución del script
inyectar_estilos()

# =============================================================================
# MENÚ LATERAL DE NAVEGACIÓN
# -----------------------------------------------------------------------------
# Se usa st.radio estilizado como "píldoras" modernas (ver CSS). El texto de
# cada opción es descriptivo (E1, E2, ...) y el diccionario lo traduce a la
# sección interna correspondiente.
# =============================================================================
OPCIONES_MENU = {
    "🏠  Home": "Home",
    "💰  E1 · Flujo de Caja": "Ejercicio 1",
    "📦  E2 · Registro NumPy": "Ejercicio 2",
    "📊  E3 · Préstamo Francés": "Ejercicio 3",
    "🏗️  E4 · CRUD Inversiones": "Ejercicio 4",
}

with st.sidebar:
    st.markdown(
        f"""
        <div class="marca-sidebar">
          <img src="data:image/png;base64,{LOGO_BASE64}" alt="logo"/>
          <div>
            <div class="marca-nombre">Proyecto 1</div>
            <div class="marca-sub">Python for Analytics</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("##### Navegación")
    opcion_menu = st.radio(
        "Selecciona una sección:",
        list(OPCIONES_MENU.keys()),
        label_visibility="collapsed",
        help="Cada sección corresponde a un ejercicio del Módulo 1."
    )
    seccion = OPCIONES_MENU[opcion_menu]
    registrar_cambio_de_seccion(seccion)
    st.markdown("---")
    st.caption("Otto Morales Gómez · Perú 🇵🇪 · 2026")


# =============================================================================
# SECCIÓN HOME
# =============================================================================
def mostrar_home():
    """Muestra la página de presentación del proyecto."""
    encabezado_hero(
        "Módulo 1 · Python Fundamentals",
        "Proyecto 1 - Aplicación Interactiva en Streamlit",
        "Especialización Python for Analytics · Variables, estructuras de datos, "
        "funciones y POO"
    )

    st.markdown(
            """
            <div class="tarjeta-home">
              <h3 style="margin-top:0;">👨‍💼 Información del estudiante</h3>
              <table>
                <tr><td class="campo">Nombre</td><td>Otto Morales Gómez</td></tr>
                <tr><td class="campo">Módulo</td><td>Módulo 1 - Python Fundamentals</td></tr>
                <tr><td class="campo">Curso</td><td>Especialización Python for Analytics</td></tr>
                <tr><td class="campo">Perfil</td><td>Ingeniero y MBA</td></tr>
                <tr><td class="campo">País</td><td>Perú 🇵🇪</td></tr>
                <tr><td class="campo">Año</td><td>2026</td></tr>
              </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown("""
    ### 📋 Descripción del proyecto

    Esta aplicación integra los conceptos fundamentales aprendidos en el
    Módulo 1: **variables, estructuras de datos, control de flujo, funciones,
    programación funcional y programación orientada a objetos (POO)**,
    presentados en una interfaz interactiva desarrollada con Streamlit.

    Los montos se expresan en soles con el formato oficial peruano
    (**es_PE**): `S/ 1,500.75`.

    ### 🧩 Secciones de la aplicación

    - **Ejercicio 1:** Flujo de caja con listas.
    - **Ejercicio 2:** Registro de productos con arrays de NumPy y DataFrame.
    - **Ejercicio 3:** Cálculo de la cuota de un préstamo (sistema francés) usando una función de librería externa.
    - **Ejercicio 4:** CRUD de proyectos de inversión usando una clase (POO).

    ### 🛠️ Tecnologías utilizadas

    - Python 3 · Streamlit · Pandas · NumPy
    """)


# =============================================================================
# EJERCICIO 1 - FLUJO DE CAJA CON LISTAS
# =============================================================================
def agregar_movimiento() -> None:
    """
    Callback del boton "Agregar movimiento": valida los datos, registra el
    movimiento en la lista y deja el formulario limpio para el siguiente.
    """
    concepto_limpio = limpiar_texto(st.session_state.e1_concepto)
    valor = float(st.session_state.e1_valor)

    # Validación: concepto no vacío y valor mayor a cero
    if concepto_limpio == "":
        apilar_mensaje("msg_e1", "error", "⚠️ Debes ingresar un concepto válido.")
        return
    if valor <= 0:
        apilar_mensaje("msg_e1", "error", "⚠️ El valor debe ser mayor a cero.")
        return

    try:
        st.session_state.movimientos.append({
            "Concepto": concepto_limpio,
            "Tipo": st.session_state.e1_tipo,
            "Valor (S/)": valor
        })
        apilar_mensaje(
            "msg_e1", "ok",
            f"✅ Movimiento '{concepto_limpio}' agregado correctamente."
        )
        reiniciar_campos("e1_")   # el formulario vuelve a su estado inicial
    except Exception as error:
        apilar_mensaje("msg_e1", "error",
                       f"⚠️ No se pudo registrar el movimiento: {error}")


def limpiar_movimientos() -> None:
    """Vacía la lista de movimientos del Ejercicio 1."""
    st.session_state.movimientos = []


def mostrar_ejercicio1():
    """Registra ingresos y gastos en una lista y calcula el saldo final."""
    encabezado_hero(
        "E1 · Listas",
        "Flujo de Caja",
        "Registro de ingresos y gastos con listas de Python y cálculo del saldo final"
    )

    st.markdown("""
    **Descripción:** este módulo registra movimientos financieros
    (ingresos y gastos) en una **lista**. Cada movimiento se guarda como un
    diccionario con su concepto, tipo y valor. Al final se calcula el total
    de ingresos, el total de gastos y el saldo, indicando si el flujo de
    caja está **a favor** o **en contra**.
    """)

    # --- Formulario de ingreso de datos ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input(
            "Concepto del movimiento",
            placeholder="Ej: Venta de servicios",
            max_chars=MAX_CARACTERES_TEXTO,
            key="e1_concepto",
            help="Descripción breve del movimiento (máx. 60 caracteres)."
        )
    with col2:
        st.selectbox(
            "Tipo de movimiento",
            ["Ingreso", "Gasto"],
            key="e1_tipo",
            help="Ingreso: entrada de dinero. Gasto: salida de dinero."
        )
    with col3:
        valor = st.number_input(
            "Valor (S/)",
            min_value=0.0,
            max_value=MAX_MONTO,
            step=10.0,
            format="%.2f",
            key="e1_valor",
            help="Monto en soles, mayor a cero."
        )
        st.caption(f"Se registrará: **{formatear_moneda(valor)}**")

    # --- Botón para agregar el movimiento a la lista ---
    # El registro se hace en un callback (on_click) para poder limpiar los
    # campos del formulario inmediatamente después de guardar.
    st.button("➕ Agregar movimiento", on_click=agregar_movimiento)
    mostrar_mensajes("msg_e1")

    st.markdown("---")

    # --- Resultados: solo se muestran si la lista tiene movimientos ---
    if len(st.session_state.movimientos) > 0:
        st.subheader("📄 Movimientos registrados")
        try:
            # La lista de diccionarios se convierte en DataFrame (tabla)
            df_movimientos = pd.DataFrame(st.session_state.movimientos)
            df_vista = df_movimientos.copy()
            df_vista["Valor (S/)"] = df_vista["Valor (S/)"].map(formatear_moneda)
            st.dataframe(df_vista, width="stretch")

            # --- Programación funcional: generadores + sum con filtro ---
            total_ingresos = sum(
                m["Valor (S/)"] for m in st.session_state.movimientos
                if m["Tipo"] == "Ingreso"
            )
            total_gastos = sum(
                m["Valor (S/)"] for m in st.session_state.movimientos
                if m["Tipo"] == "Gasto"
            )
            saldo = total_ingresos - total_gastos

            # --- Métricas en pantalla ---
            c1, c2, c3 = st.columns(3)
            c1.metric("Total ingresos", formatear_moneda(total_ingresos))
            c2.metric("Total gastos", formatear_moneda(total_gastos))
            c3.metric("Saldo final", formatear_moneda(saldo))

            # --- Control de flujo: el saldo define el mensaje final ---
            if saldo >= 0:
                st.success(f"✅ El flujo de caja está **A FAVOR** por {formatear_moneda(saldo)}")
            else:
                st.error(f"❌ El flujo de caja está **EN CONTRA** por {formatear_moneda(abs(saldo))}")
        except Exception as error:
            st.error(f"⚠️ Ocurrió un error al procesar los movimientos: {error}")

        # Botón para reiniciar la lista de movimientos (pide confirmación)
        boton_limpiar_confirmado(
            "🗑️ Limpiar movimientos",
            "e1",
            limpiar_movimientos,
            f"⚠️ Se eliminarán los {len(st.session_state.movimientos)} movimientos "
            "registrados. Esta acción no se puede deshacer. ¿Deseas continuar?"
        )
    else:
        st.info("ℹ️ Aún no hay movimientos registrados. Agrega el primero arriba.")


# =============================================================================
# EJERCICIO 2 - REGISTRO CON NUMPY, ARRAYS Y DATAFRAME
# =============================================================================
def agregar_producto() -> None:
    """
    Callback del boton "Agregar registro": valida, agrega el producto a los
    arrays de NumPy y deja el formulario limpio para el siguiente ingreso.
    """
    nombre_limpio = limpiar_texto(st.session_state.e2_nombre)
    precio = float(st.session_state.e2_precio)
    cantidad = int(st.session_state.e2_cantidad)

    if nombre_limpio == "":
        apilar_mensaje("msg_e2", "error",
                       "⚠️ Debes ingresar un nombre de producto válido.")
        return
    if precio <= 0:
        apilar_mensaje("msg_e2", "error", "⚠️ El precio debe ser mayor a cero.")
        return

    try:
        # Advertencia (no bloqueo) si el producto ya fue registrado antes
        if nombre_limpio in st.session_state.arr_productos:
            apilar_mensaje(
                "msg_e2", "aviso",
                f"ℹ️ '{nombre_limpio}' ya estaba registrado; "
                "se agregó como un registro adicional."
            )
        total = precio * cantidad
        # np.append crea un nuevo array agregando el elemento al final
        st.session_state.arr_productos = np.append(st.session_state.arr_productos, nombre_limpio)
        st.session_state.arr_categorias = np.append(st.session_state.arr_categorias, st.session_state.e2_categoria)
        st.session_state.arr_precios = np.append(st.session_state.arr_precios, precio)
        st.session_state.arr_cantidades = np.append(st.session_state.arr_cantidades, cantidad)
        st.session_state.arr_totales = np.append(st.session_state.arr_totales, total)
        apilar_mensaje("msg_e2", "ok",
                       f"✅ Producto '{nombre_limpio}' registrado correctamente.")
        reiniciar_campos("e2_")   # el formulario vuelve a su estado inicial
    except Exception as error:
        apilar_mensaje("msg_e2", "error",
                       f"⚠️ No se pudo registrar el producto: {error}")


def limpiar_registros() -> None:
    """Vacía los cinco arrays de NumPy del Ejercicio 2."""
    st.session_state.arr_productos = np.array([], dtype=object)
    st.session_state.arr_categorias = np.array([], dtype=object)
    st.session_state.arr_precios = np.array([], dtype=float)
    st.session_state.arr_cantidades = np.array([], dtype=int)
    st.session_state.arr_totales = np.array([], dtype=float)


def mostrar_ejercicio2():
    """Registra productos en arrays de NumPy y los muestra en un DataFrame."""
    encabezado_hero(
        "E2 · NumPy",
        "Registro de Productos",
        "Arrays de NumPy convertidos en un DataFrame de Pandas actualizado en vivo"
    )

    st.markdown("""
    **Descripción:** este formulario registra productos usando **arrays de
    NumPy** (un array por cada campo). Con cada registro, los arrays se
    actualizan con `np.append()` y luego se convierten en un **DataFrame**
    de Pandas que se muestra actualizado en pantalla.
    """)

    # --- Formulario de ingreso de datos ---
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(
            "Nombre del producto",
            placeholder="Ej: Laptop",
            max_chars=MAX_CARACTERES_TEXTO,
            key="e2_nombre",
            help="Nombre del producto o servicio (máx. 60 caracteres)."
        )
        st.selectbox(
            "Categoría",
            ["Tecnología", "Alimentos", "Ropa", "Hogar", "Servicios", "Otros"],
            key="e2_categoria",
            help="Clasificación del producto para el análisis por categoría."
        )
    with col2:
        precio = st.number_input(
            "Precio unitario (S/)",
            min_value=0.0,
            max_value=MAX_MONTO,
            step=1.0,
            format="%.2f",
            key="e2_precio",
            help="Precio de venta por unidad, en soles."
        )
        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            max_value=1_000_000,
            step=1,
            key="e2_cantidad",
            help="Número de unidades del registro (entero, mínimo 1)."
        )

    # El total se calcula automáticamente: precio × cantidad
    total = float(precio) * int(cantidad)
    st.markdown(f"**Total del registro:** {formatear_moneda(total)}")

    # --- Botón para agregar el registro a los arrays ---
    st.button("➕ Agregar registro", on_click=agregar_producto)
    mostrar_mensajes("msg_e2")

    st.markdown("---")

    # --- Tabla actualizada: los arrays se convierten en DataFrame ---
    if st.session_state.arr_productos.size > 0:
        st.subheader("📄 Registros almacenados (arrays → DataFrame)")
        try:
            df_registros = pd.DataFrame({
                "Producto": st.session_state.arr_productos,
                "Categoría": st.session_state.arr_categorias,
                "Precio (S/)": [formatear_moneda(p) for p in st.session_state.arr_precios],
                "Cantidad": st.session_state.arr_cantidades,
                "Total (S/)": [formatear_moneda(t) for t in st.session_state.arr_totales],
            })
            st.dataframe(df_registros, width="stretch")

            # Estadísticas con operaciones vectorizadas de NumPy
            c1, c2, c3 = st.columns(3)
            c1.metric("Registros", int(st.session_state.arr_productos.size))
            c2.metric("Venta total", formatear_moneda(st.session_state.arr_totales.sum()))
            c3.metric("Ticket promedio", formatear_moneda(st.session_state.arr_totales.mean()))
        except Exception as error:
            st.error(f"⚠️ Ocurrió un error al mostrar los registros: {error}")

        boton_limpiar_confirmado(
            "🗑️ Limpiar registros",
            "e2",
            limpiar_registros,
            f"⚠️ Se eliminarán los {int(st.session_state.arr_productos.size)} "
            "productos registrados. Esta acción no se puede deshacer. "
            "¿Deseas continuar?"
        )
    else:
        st.info("ℹ️ Aún no hay registros. Agrega el primer producto arriba.")


# =============================================================================
# EJERCICIO 3 - FUNCIÓN DE LIBRERÍA EXTERNA: CUOTA DE PRÉSTAMO (SISTEMA FRANCÉS)
# =============================================================================
def calcular_y_registrar_prestamo() -> None:
    """
    Callback del boton "Calcular cuota": ejecuta la funcion de la libreria,
    guarda el resultado en el historico y deja los parametros en sus valores
    iniciales para el siguiente escenario.
    """
    monto = float(st.session_state.e3_monto)
    tasa = float(st.session_state.e3_tasa)
    plazo = int(st.session_state.e3_plazo)

    # Validación previa: el monto y el plazo deben ser mayores a cero
    if monto <= 0 or plazo <= 0:
        apilar_mensaje("msg_e3", "error",
                       "⚠️ El monto y el plazo deben ser mayores a cero.")
        return

    try:
        resultado = calcular_cuota_prestamo_frances(
            monto=monto,
            tasa_anual_pct=tasa,
            plazo_meses=plazo
        )
        cuota = resultado["cuota_mensual"]
        total_pagado = resultado["total_pagado"]
        interes_total = resultado["interes_total"]

        # El resultado se guarda para dibujarlo apenas termine el callback
        st.session_state.ultimo_prestamo = resultado
        apilar_mensaje(
            "msg_e3", "ok",
            f"✅ La cuota mensual es **{formatear_moneda(cuota)}** durante "
            f"{plazo} meses. Se pagará un interés total de "
            f"**{formatear_moneda(interes_total)}**."
        )

        # --- Se agrega el resultado al histórico (con tope) ---
        st.session_state.historico_prestamo.append({
            "Monto (S/)": monto,
            "Tasa anual (%)": tasa,
            "Plazo (meses)": plazo,
            "Cuota mensual (S/)": cuota,
            "Total pagado (S/)": total_pagado,
            "Interés total (S/)": interes_total
        })
        if len(st.session_state.historico_prestamo) > MAX_REGISTROS_HISTORICO:
            st.session_state.historico_prestamo.pop(0)

        reiniciar_campos("e3_")   # los parámetros vuelven a su valor inicial
    except (ValueError, ZeroDivisionError) as error:
        # Validaciones internas de la librería o división inválida
        apilar_mensaje("msg_e3", "error",
                       f"⚠️ Error en los datos ingresados: {error}")
    except Exception as error:
        apilar_mensaje("msg_e3", "error",
                       f"⚠️ Error inesperado al calcular la cuota: {error}")


def limpiar_historico_prestamo() -> None:
    """Vacía el histórico de cálculos del Ejercicio 3."""
    st.session_state.historico_prestamo = []


def mostrar_ejercicio3():
    """Conecta la función calcular_cuota_prestamo_frances() de la librería con widgets."""
    encabezado_hero(
        "E3 · Función externa",
        "Cuota de Préstamo (Sistema Francés)",
        "Cálculo de la cuota mensual con calcular_cuota_prestamo_frances() de la librería del curso"
    )

    st.markdown("""
    **Descripción:** se utiliza la función `calcular_cuota_prestamo_frances()`
    del archivo `libreria_funciones_proyecto1.py`, seleccionada por su relación
    con el área financiera. El **sistema francés** es el método de amortización
    más usado: se paga una **cuota mensual fija** que combina capital e
    intereses durante todo el plazo del préstamo.

    **Fórmula:**  `Cuota = M × [ i × (1 + i)ⁿ ] / [ (1 + i)ⁿ − 1 ]`

    donde **M** = monto del préstamo, **i** = tasa de interés mensual
    (tasa anual ÷ 12) y **n** = número de cuotas (plazo en meses).
    """)

    # --- Selector de función (requisito de la interfaz) ---
    st.selectbox(
        "Función seleccionada de la librería:",
        ["calcular_cuota_prestamo_frances - Cuota mensual de un préstamo"],
        help="Función elegida de libreria_funciones_proyecto1.py (área financiera)."
    )

    # --- Widgets para ingresar los parámetros de la función ---
    col1, col2 = st.columns(2)
    with col1:
        st.number_input(
            "Monto del préstamo (S/)",
            min_value=0.0, max_value=MAX_MONTO, step=1000.0,
            key="e3_monto",
            help="M: capital solicitado en préstamo."
        )
        st.number_input(
            "Tasa de interés anual (%)",
            min_value=0.0, max_value=100.0,
            key="e3_tasa",
            help="Tasa nominal anual. Se divide entre 12 para obtener la tasa mensual."
        )
    with col2:
        st.number_input(
            "Plazo (meses)",
            min_value=1, max_value=600, step=1,
            key="e3_plazo",
            help="n: número de cuotas mensuales en las que se pagará el préstamo."
        )

    # --- Botón para ejecutar la función ---
    st.button("🧮 Calcular cuota", on_click=calcular_y_registrar_prestamo)

    # --- Resultado en pantalla (solo en la corrida posterior al cálculo) ---
    prestamo_reciente = st.session_state.pop("ultimo_prestamo", None)
    if prestamo_reciente is not None:
        m1, m2, m3 = st.columns(3)
        m1.metric("Cuota mensual", formatear_moneda(prestamo_reciente["cuota_mensual"]))
        m2.metric("Total pagado", formatear_moneda(prestamo_reciente["total_pagado"]))
        m3.metric("Interés total", formatear_moneda(prestamo_reciente["interes_total"]))
    mostrar_mensajes("msg_e3")

    st.markdown("---")

    # --- Tabla histórica de resultados ---
    if len(st.session_state.historico_prestamo) > 0:
        st.subheader("📄 Histórico de cálculos")
        try:
            df_historico = pd.DataFrame(st.session_state.historico_prestamo)
            df_vista = df_historico.copy()
            for col in ("Monto (S/)", "Cuota mensual (S/)",
                        "Total pagado (S/)", "Interés total (S/)"):
                df_vista[col] = df_vista[col].map(formatear_moneda)
            st.dataframe(df_vista, width="stretch")
        except Exception as error:
            st.error(f"⚠️ No se pudo mostrar el histórico: {error}")

        boton_limpiar_confirmado(
            "🗑️ Limpiar histórico",
            "e3",
            limpiar_historico_prestamo,
            f"⚠️ Se eliminarán los {len(st.session_state.historico_prestamo)} cálculos "
            "del histórico. Esta acción no se puede deshacer. ¿Deseas continuar?"
        )
    else:
        st.info("ℹ️ Aún no hay cálculos en el histórico.")


# =============================================================================
# EJERCICIO 4 - CLASE DE LIBRERÍA EXTERNA CON CRUD: ProyectoInversion
# =============================================================================
def crear_proyecto() -> None:
    """
    Callback del boton "Crear proyecto": instancia el objeto
    ProyectoInversion, lo guarda en el diccionario y limpia el formulario.
    """
    nombre_limpio = limpiar_texto(st.session_state.e4_nombre)
    anios = int(st.session_state.e4_anios)
    flujos = [float(st.session_state[f"flujo_{i}"]) for i in range(anios)]

    if nombre_limpio == "":
        apilar_mensaje("msg_e4", "error",
                       "⚠️ Debes ingresar un nombre de proyecto válido.")
        return
    if nombre_limpio in st.session_state.proyectos:
        apilar_mensaje("msg_e4", "error",
                       "⚠️ Ya existe un proyecto con ese nombre. "
                       "Usa 'Actualizar' para modificarlo.")
        return
    if sum(flujos) <= 0:
        # Guarda: el payback divide entre el flujo promedio; con todos
        # los flujos en cero se produciría una división entre cero.
        apilar_mensaje("msg_e4", "error",
                       "⚠️ Al menos un flujo anual debe ser mayor a cero.")
        return

    try:
        # Se instancia el objeto y se guarda en el diccionario
        proyecto = ProyectoInversion(
            nombre_proyecto=nombre_limpio,
            inversion_inicial=float(st.session_state.e4_inversion),
            flujos=flujos,
            tasa_descuento_pct=float(st.session_state.e4_tasa)
        )
        st.session_state.proyectos[nombre_limpio] = proyecto
        apilar_mensaje("msg_e4", "ok",
                       f"✅ Proyecto '{nombre_limpio}' creado correctamente.")
        reiniciar_campos("e4_", "flujo_")   # formulario limpio
    except (ValueError, ZeroDivisionError) as error:
        apilar_mensaje("msg_e4", "error", f"⚠️ Error al crear el proyecto: {error}")
    except Exception as error:
        apilar_mensaje("msg_e4", "error",
                       f"⚠️ Error inesperado al crear el proyecto: {error}")


def eliminar_proyecto() -> None:
    """Quita del diccionario el proyecto seleccionado en la pestaña Eliminar."""
    nombre = st.session_state.get("sel_eliminar", "")
    try:
        # del elimina la clave (y su objeto) del diccionario
        del st.session_state.proyectos[nombre]
        apilar_mensaje("msg_e4_del", "ok", f"✅ Proyecto '{nombre}' eliminado.")
    except KeyError:
        apilar_mensaje("msg_e4_del", "error",
                       "⚠️ El proyecto ya no existe en el registro.")


def mostrar_ejercicio4():
    """CRUD de proyectos de inversión usando la clase ProyectoInversion."""
    encabezado_hero(
        "E4 · POO + CRUD",
        "Proyectos de Inversión",
        "Crear, leer, actualizar y eliminar proyectos con la clase ProyectoInversion "
        "(VPN, ROI y Payback)"
    )

    st.markdown("""
    **Descripción:** se utiliza la clase `ProyectoInversion` del archivo
    `libreria_clases_proyecto1.py`. Cada proyecto se crea como un **objeto**
    con nombre, inversión inicial, flujos anuales y tasa de descuento, y sus
    métodos calculan el **VPN**, el **ROI** y el **Payback**. Se implementan
    las cuatro operaciones **CRUD**: Crear, Leer, Actualizar y Eliminar.
    """)

    # Las 4 operaciones CRUD se organizan en pestañas
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(
        ["➕ Crear", "📖 Leer", "✏️ Actualizar", "🗑️ Eliminar"]
    )

    # -------------------------------------------------------------------------
    # CREAR: registra un nuevo objeto ProyectoInversion
    # -------------------------------------------------------------------------
    with tab_crear:
        st.subheader("Crear un nuevo proyecto")

        st.text_input(
            "Nombre del proyecto",
            placeholder="Ej: Planta de Arequipa",
            max_chars=MAX_CARACTERES_TEXTO,
            key="e4_nombre",
            help="Identificador único del proyecto (máx. 60 caracteres)."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Inversión inicial (S/)",
                min_value=0.0, max_value=MAX_MONTO, step=5000.0,
                key="e4_inversion",
                help="Desembolso en el año 0. Debe ser mayor a cero."
            )
            st.number_input(
                "Tasa de descuento (%)",
                min_value=0.0, max_value=100.0,
                key="e4_tasa",
                help="Tasa para traer los flujos a valor presente; "
                     "usualmente el WACC o el costo de oportunidad (COK)."
            )
        with col2:
            anios = st.number_input(
                "Número de años de flujos",
                min_value=1, max_value=MAX_ANIOS_FLUJOS,
                key="e4_anios",
                help=f"Horizonte de evaluación del proyecto (1 a {MAX_ANIOS_FLUJOS} años)."
            )

        # Se genera un number_input por cada año de flujo proyectado
        st.markdown("**Flujos de caja anuales proyectados (S/):**")
        columnas_flujos = st.columns(int(anios))
        for i, col in enumerate(columnas_flujos):
            with col:
                st.number_input(
                    f"Año {i + 1}",
                    min_value=0.0, max_value=MAX_MONTO,
                    step=5000.0, key=f"flujo_{i}",
                    help=f"Flujo de caja neto esperado del año {i + 1}."
                )

        st.button("➕ Crear proyecto", on_click=crear_proyecto)
        mostrar_mensajes("msg_e4")

    # -------------------------------------------------------------------------
    # LEER: muestra todos los proyectos con sus indicadores calculados
    # -------------------------------------------------------------------------
    with tab_leer:
        st.subheader("Proyectos registrados")

        if len(st.session_state.proyectos) > 0:
            try:
                # El método resumen() de cada objeto devuelve un diccionario
                # con VPN, ROI, Payback y la decisión (Viable / No viable)
                resumenes = [p.resumen() for p in st.session_state.proyectos.values()]
                df_proyectos = pd.DataFrame(resumenes)
                df_proyectos.columns = ["Proyecto", "VPN (S/)", "ROI (%)",
                                        "Payback (años)", "Decisión"]
                df_vista = df_proyectos.copy()
                df_vista["VPN (S/)"] = df_vista["VPN (S/)"].map(formatear_moneda)
                st.dataframe(df_vista, width="stretch")

                # Detalle individual del proyecto seleccionado
                seleccionado = st.selectbox(
                    "Ver detalle de:",
                    list(st.session_state.proyectos.keys()),
                    help="Selecciona un proyecto para ver sus indicadores."
                )
                resumen = st.session_state.proyectos[seleccionado].resumen()

                c1, c2, c3 = st.columns(3)
                c1.metric(
                    "VPN", formatear_moneda(resumen["vpn"]),
                    help="Valor Presente Neto: valor que el proyecto crea "
                         "(VPN > 0) o destruye (VPN < 0) a la tasa de descuento."
                )
                c2.metric(
                    "ROI", f"{formatear_numero(resumen['roi_pct'])} %",
                    help="Retorno sobre la inversión: utilidad total de los "
                         "flujos respecto de la inversión inicial."
                )
                c3.metric(
                    "Payback", f"{formatear_numero(resumen['payback_anios'])} años",
                    help="Años necesarios para recuperar la inversión "
                         "(método simple, con flujo promedio)."
                )

                if resumen["decision"] == "Viable":
                    st.success(f"✅ El proyecto '{seleccionado}' es **VIABLE** (VPN positivo).")
                else:
                    st.error(f"❌ El proyecto '{seleccionado}' **NO es viable** (VPN negativo).")

                # -------------------------------------------------------------
                # Flujo de caja del proyecto (año 0 = inversión inicial)
                # -------------------------------------------------------------
                # Se reconstruye el cronograma a partir de los atributos del
                # objeto para validar el VPN año por año: la última fila de la
                # columna "VPN acumulado" coincide con la métrica VPN de arriba.
                st.markdown("---")
                st.subheader("📆 Flujo de caja del proyecto")

                proyecto_sel = st.session_state.proyectos[seleccionado]
                tasa = proyecto_sel.tasa_descuento_pct / 100

                filas_flujo = []
                vpn_acumulado = 0.0
                # Año 0: la inversión inicial se registra como salida (negativa)
                flujos_completos = [-proyecto_sel.inversion_inicial] + list(proyecto_sel.flujos)
                for anio, flujo in enumerate(flujos_completos):
                    factor = 1 / ((1 + tasa) ** anio)
                    valor_presente = flujo * factor
                    vpn_acumulado += valor_presente
                    filas_flujo.append({
                        "Año": anio,
                        "Flujo (S/)": round(flujo, 2),
                        "Factor descuento": round(factor, 6),
                        "Valor presente (S/)": round(valor_presente, 2),
                        "VPN acumulado (S/)": round(vpn_acumulado, 2),
                    })

                df_flujo = pd.DataFrame(filas_flujo)

                # Vista con montos formateados en soles
                df_flujo_vista = df_flujo.copy()
                for col in ("Flujo (S/)", "Valor presente (S/)", "VPN acumulado (S/)"):
                    df_flujo_vista[col] = df_flujo_vista[col].map(formatear_moneda)
                st.dataframe(df_flujo_vista, width="stretch", hide_index=True)

                st.caption(
                    f"💡 La última fila de **VPN acumulado** "
                    f"({formatear_moneda(vpn_acumulado)}) coincide con el VPN "
                    f"calculado por el método `calcular_vpn()` de la clase. "
                    f"Tasa de descuento: {formatear_numero(proyecto_sel.tasa_descuento_pct)}%."
                )

                # Botón de descarga: CSV con los valores numéricos (sin formato)
                csv_flujo = df_flujo.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "⬇️ Descargar flujo de caja (CSV)",
                    data=csv_flujo,
                    file_name=f"flujo_caja_{seleccionado}.csv",
                    mime="text/csv"
                )
            except (ValueError, ZeroDivisionError) as error:
                st.error(f"⚠️ Error al calcular los indicadores: {error}")
            except Exception as error:
                st.error(f"⚠️ Error inesperado al mostrar los proyectos: {error}")
        else:
            st.info("ℹ️ No hay proyectos registrados. Crea uno en la pestaña 'Crear'.")

    # -------------------------------------------------------------------------
    # ACTUALIZAR: modifica los atributos de un proyecto existente
    # -------------------------------------------------------------------------
    with tab_actualizar:
        st.subheader("Actualizar un proyecto existente")

        if len(st.session_state.proyectos) > 0:
            nombre_actualizar = st.selectbox(
                "Proyecto a actualizar:",
                list(st.session_state.proyectos.keys()),
                key="sel_actualizar",
                help="Los campos se precargan con los valores actuales del proyecto."
            )
            proyecto_actual = st.session_state.proyectos[nombre_actualizar]

            # Los campos se precargan con los valores actuales del objeto
            col1, col2 = st.columns(2)
            with col1:
                nueva_inversion = st.number_input(
                    "Nueva inversión inicial (S/)",
                    min_value=0.0, max_value=MAX_MONTO,
                    value=float(proyecto_actual.inversion_inicial),
                    step=5000.0,
                    key="upd_inversion",
                    help="Desembolso en el año 0. Debe ser mayor a cero."
                )
            with col2:
                nueva_tasa = st.number_input(
                    "Nueva tasa de descuento (%)",
                    min_value=0.0, max_value=100.0,
                    value=float(proyecto_actual.tasa_descuento_pct),
                    key="upd_tasa",
                    help="Tasa para descontar los flujos (WACC o COK)."
                )

            st.markdown("**Flujos de caja anuales (S/):**")
            nuevos_flujos = []
            columnas_upd = st.columns(len(proyecto_actual.flujos))
            for i, col in enumerate(columnas_upd):
                with col:
                    flujo = st.number_input(
                        f"Año {i + 1}",
                        min_value=0.0, max_value=MAX_MONTO,
                        value=float(proyecto_actual.flujos[i]),
                        step=5000.0,
                        key=f"upd_flujo_{i}",
                        help=f"Flujo de caja neto esperado del año {i + 1}."
                    )
                    nuevos_flujos.append(float(flujo))

            if st.button("✏️ Guardar cambios"):
                if sum(nuevos_flujos) <= 0:
                    st.error("⚠️ Al menos un flujo anual debe ser mayor a cero.")
                else:
                    try:
                        # Se reemplaza el objeto por uno nuevo con los datos actualizados
                        st.session_state.proyectos[nombre_actualizar] = ProyectoInversion(
                            nombre_proyecto=nombre_actualizar,
                            inversion_inicial=nueva_inversion,
                            flujos=nuevos_flujos,
                            tasa_descuento_pct=nueva_tasa
                        )
                        st.success(f"✅ Proyecto '{nombre_actualizar}' actualizado correctamente.")
                    except (ValueError, ZeroDivisionError) as error:
                        st.error(f"⚠️ Error al actualizar: {error}")
                    except Exception as error:
                        st.error(f"⚠️ Error inesperado al actualizar: {error}")
        else:
            st.info("ℹ️ No hay proyectos para actualizar.")

    # -------------------------------------------------------------------------
    # ELIMINAR: quita un proyecto del diccionario
    # -------------------------------------------------------------------------
    with tab_eliminar:
        st.subheader("Eliminar un proyecto")

        if len(st.session_state.proyectos) > 0:
            nombre_eliminar = st.selectbox(
                "Proyecto a eliminar:",
                list(st.session_state.proyectos.keys()),
                key="sel_eliminar",
                help="Esta acción quita el proyecto del registro de la sesión."
            )
            boton_limpiar_confirmado(
                "🗑️ Eliminar proyecto",
                "e4",
                eliminar_proyecto,
                f"⚠️ Se eliminará definitivamente el proyecto "
                f"'{nombre_eliminar}'. ¿Deseas continuar?"
            )
        else:
            st.info("ℹ️ No hay proyectos para eliminar.")

        # El mensaje se muestra fuera del if para que también sea visible
        # cuando se elimina el último proyecto del registro.
        mostrar_mensajes("msg_e4_del")


# =============================================================================
# ENRUTAMIENTO PRINCIPAL
# -----------------------------------------------------------------------------
# Según la opción elegida en el menú lateral, se llama a la función que
# dibuja la sección correspondiente. Un try/except global evita que un
# error no previsto muestre un traceback crudo al usuario final.
# =============================================================================
SECCIONES = {
    "Home": mostrar_home,
    "Ejercicio 1": mostrar_ejercicio1,
    "Ejercicio 2": mostrar_ejercicio2,
    "Ejercicio 3": mostrar_ejercicio3,
    "Ejercicio 4": mostrar_ejercicio4,
}

try:
    SECCIONES.get(seccion, mostrar_home)()
except Exception as error_global:
    st.error(
        "🚫 Ocurrió un error no previsto en la aplicación. "
        f"Detalle técnico: `{error_global}`"
    )

st.markdown(
    '<div class="pie-pagina">Proyecto 1 · Especialización Python for Analytics · '
    'Otto Morales Gómez · Perú 🇵🇪 · 2026</div>',
    unsafe_allow_html=True,
)
