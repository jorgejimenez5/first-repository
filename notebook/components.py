# components.py
import streamlit as st

def render_header():
    st.markdown(
        """
        <div class="header">
          <h1>📊 Plataforma de Análisis Estratégico</h1>
          <p class="muted">
            Análisis y Sistematización de Puntos Críticos por Cadena de Valor y Eslabón
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_kpis(df, dep_col, cad_col):
    total_rows = len(df)
    unique_deps = df[dep_col].nunique()
    unique_cadenas = df[cad_col].nunique()

    with st.container():
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Registros</div>
                    <div class="kpi-value">{total_rows:,}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Departamentos</div>
                    <div class="kpi-value">{unique_deps}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Cadenas de valor</div>
                    <div class="kpi-value">{unique_cadenas}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
