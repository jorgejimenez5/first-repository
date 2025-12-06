# app.py
import streamlit as st
from helpers import load_csv_from_github, map_headers
from styles import inject_css
from components import render_header, render_kpis
from filters import render_filters
from tables import render_tables

RAW_CSV = "https://raw.githubusercontent.com/jorgejimenez5/first-repository/main/data/data.csv"

def main():
    # === Config ===
    st.set_page_config(
        page_title="Plataforma de Análisis Estratégico",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # === Estilos globales ===
    inject_css()

    # === Header ===
    render_header()

    # === Cargar datos ===
    try:
        df = load_csv_from_github(RAW_CSV)
    except Exception as e:
        st.error(f"No se pudo cargar la base desde GitHub: {e}")
        st.stop()

    cols = map_headers(df)

    required_keys = ["departamento", "tipo", "cadena", "eslabon"]
    missing = [k for k in required_keys if not cols.get(k)]
    if missing:
        st.warning(
            f"No se encontraron las columnas esperadas en el CSV para: {missing}. "
            "Revisa los encabezados."
        )
        st.write("Encabezados detectados:", list(df.columns))
        st.stop()

    dep_col, cad_col = cols["departamento"], cols["cadena"]

    # === KPIs ===
    render_kpis(df, dep_col, cad_col)

    # === Layout en dos columnas ===
    col_filtros, col_resultados = st.columns([1, 4])

    with col_filtros:
        filtered_df = render_filters(df, cols)

    with col_resultados:
        render_tables(filtered_df, cols)

if __name__ == "__main__":
    main()
