# styles.py
import streamlit as st

def inject_css():
    st.markdown(
        """
        <style>
        /* Tipografía y fondo de header */
        .header {
            background: linear-gradient(90deg, #006769 0%, #9DDE8B 90%);
            padding: 30px;
            border-radius: 12px;
            color: white;
            margin-bottom: 16px;
        }
        .header h1 { margin: 0; font-size: 40px; }
        .header p { margin: 0; opacity: 0.9; }

        /* Card genérica (si la quieres usar luego) */
        .card {
            background: white;
            border-radius: 10px;
            padding: 14px;
            box-shadow: 0 6px 18px rgba(12, 23, 36, 0.08);
            margin-bottom: 16px;
        }
        
        /* KPI Card */
        .kpi-card {
            background: #40A578;
            border-radius: 10px;
            padding: 14px 16px;
            box-shadow: 0 6px 18px rgba(12, 23, 36, 0.08);
            margin-bottom: 20px;
            color: white;
        }

        .kpi-label {
            font-size: 13px;
            opacity: 0.8;
            margin-bottom: 4px;
        }

        .kpi-value {
            font-size: 22px;
            font-weight: 600;
        }

        /* Contenedor para alinear el botón de borrar filtros */
        .clear-btn-wrapper {
            text-align: right;
            margin-bottom: 8px;
        }

        /* Estilo del botón de borrar filtros */
        .clear-btn-wrapper button {
            background: #fee2e2;
            color: #b91c1c;
            border-radius: 999px;
            border: 1px solid #fecaca;
            padding: 4px 12px;
            font-size: 13px;
            cursor: pointer;
        }

        /* Efecto hover */
        .clear-btn-wrapper button:hover {
            background: #fecaca;
        }

        /* Pills (por si las usas más adelante) */
        .pill {
            display: inline-block;
            background: #eef2f7;
            color: #0b1220;
            padding: 6px 10px;
            border-radius: 999px;
            margin-right: 6px;
            font-size: 13px;
        }

        /* Small muted text */
        .muted { color: white; font-size: 13px; }

        /* Detail box monospace */
        .mono { font-family: monospace; white-space: pre-wrap; font-size: 13px; }

        /* Ajuste de layout de métricas (si lo necesitas luego) */
        .metrics { display:flex; gap:12px; align-items:center; }
        .metric-card { background:#f8fafc; padding:12px 14px; border-radius:8px; }
        </style>
        """,
        unsafe_allow_html=True
    )
