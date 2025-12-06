# tables.py
import streamlit as st
from helpers import to_csv

def render_html_table(df, title, filename):
    """Renderiza una tabla HTML con scroll, sin índice y con wrap de texto."""
    st.markdown(f"### {title}")

    # Nos aseguramos de no mostrar el índice visualmente
    df_no_index = df.reset_index(drop=True)

    # Convertimos a HTML sin índice
    table_html = df_no_index.to_html(
        index=False,
        escape=False,   # deja el texto tal cual; si no tienes HTML dentro, no hay problema
        classes="diag-table"
    )

    # Lo embebemos en un contenedor con scroll
    st.markdown(
        f"""
        <div class="scroll-table-container">
            {table_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Botón de descarga
    st.download_button(
        f"⬇️ Exportar {title} CSV",
        data=to_csv(df_no_index),
        file_name=filename,
        mime="text/csv",
    )

def render_tables(filtered_df, cols):
    if filtered_df is None or filtered_df.empty:
        st.info("No hay datos que coincidan con los filtros seleccionados.")
        return

    # === TABLA DIAGNÓSTICO ===
    diag_keys = [
        "departamento",
        "tipo",
        "cadena",
        "eslabon",
        "punto_critico",
        "causas",
        "impactos",
        "datos",
    ]
    diag_cols = [cols[c] for c in diag_keys if cols.get(c)]
    diag_df = filtered_df[diag_cols]

    render_html_table(
        diag_df,
        title="🧩 Diagnóstico por cadena y eslabón",
        filename="diagnostico.csv"
    )

    st.markdown("---")

    # === TABLA INTERVENCIONES ===
    int_keys = [
        "departamento",
        "tipo",
        "cadena",
        "eslabon",
        "set_interv",
        "programas",
        "actividades",
    ]
    int_cols = [cols[c] for c in int_keys if cols.get(c)]
    int_df = filtered_df[int_cols]

    render_html_table(
        int_df,
        title="🧠 Intervenciones priorizadas por cadena y eslabón",
        filename="intervenciones.csv"
    )
