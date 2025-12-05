import streamlit as st
import pandas as pd
import unicodedata
from io import BytesIO

def norm(text):
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

def map_headers(df):
    target = {
        "departamento": ["departamento", "region", "región"],
        "tipo": ["tipo"],
        "cadena": ["cadena de valor", "cadena"],
        "eslabon": ["eslabon", "eslabón", "eslabon de la cadena"],
        "programas": ["programas presupuestales", "pp involucrados"],
        "actividades": ["actividades pp 2026", "codigo - descripcion"],
        "punto_critico": ["punto critico", "punto crítico"],
        "causas": ["Causas (análisis específico)"],
        "impactos": ["Impactos (análisis específico)"],
        "datos": ["Datos Estadísticos de Sustento", "datos estadisticos", "datos de sustento"],
        "set_interv": ["Set de Intervenciones (análisis específico)", "intervenciones"],
    }
    df_cols = {norm(c): c for c in df.columns}

    def pick(aliases):
        for a in aliases:
            na = norm(a)
            if na in df_cols:
                return df_cols[na]
        return None

    return {k: pick(v) for k, v in target.items()}

def to_csv(df):
    buffer = BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8-sig')
    buffer.seek(0)
    return buffer

@st.cache_data(ttl=3600)
def load_csv_from_github(url):
    return pd.read_csv(url)
