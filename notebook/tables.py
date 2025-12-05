# tables.py
import streamlit as st
from helpers import to_csv

def render_tables(filtered_df, cols):
    if filtered_df is None or filtered_df.empty:
        st.info("No hay datos que coincidan con los filtros seleccionados.")
        return

    # === TABLA DIAGNÓSTICO ===
    st.markdown("### 🧩 Diagnóstico por cadena y eslabón")
    diag_keys = ["departamento","tipo","cadena","eslabon","punto_critico","causas","impactos","datos"]
    diag_cols = [cols[c] for c in diag_keys if cols.get(c)]
    st.dataframe(filtered_df[diag_cols], use_container_width=True)
    st.download_button(
        "⬇️ Exportar Diagnóstico CSV",
        data=to_csv(filtered_df[diag_cols]),
        file_name="diagnostico.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # === TABLA INTERVENCIONES ===
    st.markdown("### 🧠 Intervenciones priorizadas por cadena y eslabón")
    int_keys = ["departamento","tipo","cadena","eslabon","set_interv","programas","actividades"]
    int_cols = [cols[c] for c in int_keys if cols.get(c)]
    st.dataframe(filtered_df[int_cols], use_container_width=True)
    st.download_button(
        "⬇️ Exportar Intervenciones CSV",
        data=to_csv(filtered_df[int_cols]),
        file_name="intervenciones.csv",
        mime="text/csv"
    )
