# filters.py
import streamlit as st
from helpers import norm

def render_filters(df, cols):
    dep_col = cols["departamento"]
    tipo_col = cols["tipo"]
    cad_col = cols["cadena"]
    esl_col = cols["eslabon"]

    st.markdown("### 📍 Filtros")

    # Botón para borrar filtros
    st.markdown('<div class="clear-btn-wrapper">', unsafe_allow_html=True)
    clear_filters = st.button("🧹 Borrar filtros", key="clear_filters")
    st.markdown('</div>', unsafe_allow_html=True)

    # Reset de filtros
    if clear_filters:
        st.session_state["departamento"] = "Todos"
        st.session_state["tipo"] = "Todos"
        st.session_state["cadena"] = "Todos"
        st.session_state["eslabon"] = "Todos"
        st.session_state["q"] = ""
        st.rerun()

    # --- Widgets de filtro ---

    # Departamento
    deps = sorted(df[dep_col].dropna().unique().tolist())
    departamento = st.selectbox(
        "Departamento / Región",
        ["Todos"] + deps,
        key="departamento"
    )

    base_dep = df if departamento == "Todos" else df[df[dep_col] == departamento]

    st.markdown("### 🌾 Filtros por Cadena Productiva")

    # Tipo
    tipos = sorted(base_dep[tipo_col].dropna().unique().tolist())
    tipo = st.selectbox(
        "Tipo de cadena",
        ["Todos"] + tipos,
        key="tipo"
    )

    base_tipo = base_dep if tipo == "Todos" else base_dep[base_dep[tipo_col] == tipo]

    # Cadena
    cadenas = sorted(base_tipo[cad_col].dropna().unique().tolist())
    cadena = st.selectbox(
        "Cadena de valor",
        ["Todos"] + cadenas,
        key="cadena"
    )

    base_cad = base_tipo if cadena == "Todos" else base_tipo[base_tipo[cad_col] == cadena]

    # Eslabón
    eslabones = sorted(base_cad[esl_col].dropna().unique().tolist())
    eslabon = st.selectbox(
        "Eslabón",
        ["Todos"] + eslabones,
        key="eslabon"
    )

    st.markdown("### 🔍 Búsqueda global")
    q = st.text_input(
        "Filtra por actividad, PP, descripción, etc.",
        key="q"
    )

    # Filtrado final
    f = base_cad if eslabon == "Todos" else base_cad[base_cad[esl_col] == eslabon]

    if q:
        nq = norm(q)
        f = f[f.apply(
            lambda r: any(nq in norm(str(v)) for v in r.values),
            axis=1
        )]

    return f
