import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import unicodedata
import re
import logging
from typing import List, Dict, Optional

# =======================
# CONFIGURACIÓN DE LOGGING
# =======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# =======================
# CONFIGURACIÓN DE RUTAS
# =======================
class Config:
    BASE_PATH = Path("C:/Users/USUARIO/Desktop/MIDAGRI/POI_MULTIANUAL_POAAR/")
    EXPORT_PATH = Path("C:/Users/USUARIO/Desktop/MIDAGRI/PY_EXPORT_MIDAGRI/")

    BASE_FILE = "base_poi_multianual_2026_2028.xlsx"
    DISTRITOS_PRIORIZADOS_FILE = "distritos_priorizados.xlsx"
    CULTIVOS_VALIDACION_FILE = "datos_cultivos_crianzas_3.xlsx"
    CULTIVOS_PRIORIZADOS_FILE = "cp.xlsx"
    CULTIVOS_PRIORIZADOS2_FILE = "cp2.xlsx"
    INTEGRALES_FILE = "palabra_integral.xlsx"
    REPLACEMENTS_FILE = "replacements.xlsx"

# =======================
# UTILIDADES
# =======================
class DataUtils:
    @staticmethod
    def limpiar_columnas(df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"))

    @staticmethod
    def normalizar_texto(texto: Optional[str]) -> str:
        if pd.isna(texto):
            return ""
        texto = str(texto).upper()
        texto = "".join(
            c for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )
        return re.sub(r"[^\w\s]", "", texto)

    @staticmethod
    def cargar_excel(path: Path, sheet_name: int | str = 0) -> pd.DataFrame:
        df = pd.read_excel(path, sheet_name=sheet_name)
        return DataUtils.limpiar_columnas(df)

    @staticmethod
    def crear_ubigeo(df: pd.DataFrame) -> pd.Series:
        return (
            df["dep._ubigeo"].astype(str).str.zfill(2) +
            df["prov._ubigeo"].astype(str).str.zfill(2) +
            df["dis._ubigeo"].astype(str).str.zfill(2)
        ).str.zfill(6)

# =======================
# PROCESAMIENTO
# =======================
class POAARProcessor:
    def __init__(self, config: Config):
        self.config = config

    def aplicar_priorizacion_cultivos(
        self, df: pd.DataFrame,
        cultivos: List[str], cultivos2: List[str],
        replacements: Dict[str, str]
    ) -> pd.DataFrame:
        pattern1 = r"\b(" + "|".join(map(re.escape, cultivos)) + r")\b"
        pattern2 = r"\b(" + "|".join(map(re.escape, cultivos2)) + r")\b"

        df["actividad_operativa_normalizada"] = df["actividad_operativa"].apply(DataUtils.normalizar_texto)

        cultivo1 = df["actividad_operativa_normalizada"].str.extract(pattern1, expand=False)
        cultivo2 = df["actividad_operativa_normalizada"].str.extract(pattern2, expand=False)

        df["cultivo_priorizado"] = cultivo1.fillna(cultivo2).fillna("")
        df["cultivo_priorizado"] = df["cultivo_priorizado"].replace(replacements)
        df["en_cultivo_priorizado"] = df["cultivo_priorizado"].apply(lambda x: "SI" if x else "")

        df.drop(columns=["actividad_operativa_normalizada"], inplace=True)
        return df

    def aplicar_proyectos_integrales(self, df: pd.DataFrame, integrales: List[str]) -> pd.DataFrame:
        pattern = r"\b(" + "|".join(map(re.escape, integrales)) + r")\b"
        df["proyecto_integral"] = df["producto"].str.upper().str.extract(pattern, expand=False).fillna("")
        df["es_proyecto_integral"] = df["proyecto_integral"].apply(lambda x: "SI" if x else "NO")
        return df

    def marcar_articulados(self, df: pd.DataFrame) -> pd.DataFrame:
        conteo = df.groupby(["ubigeo", "cultivo_priorizado"])["actividad_operativa"].nunique().reset_index()
        conteo["articulado"] = (conteo["actividad_operativa"] > 1).astype(int)

        df = df.merge(conteo[["ubigeo", "cultivo_priorizado", "articulado"]],
                      on=["ubigeo", "cultivo_priorizado"], how="left")

        df["articulado"] = df["articulado"].fillna(0).astype(int)
        return df

# =======================
# PIPELINE PRINCIPAL
# =======================
def main():
    cfg = Config()
    processor = POAARProcessor(cfg)

    logging.info("Cargando archivos principales...")
    df = DataUtils.cargar_excel(cfg.BASE_PATH / cfg.BASE_FILE)
    df_dp = DataUtils.cargar_excel(cfg.BASE_PATH / cfg.DISTRITOS_PRIORIZADOS_FILE)
    df_dp["ubigeo"] = df_dp["ubigeo"].astype(str).str.zfill(6)

    df["es_aoi_poaar"] = df["actividad_operativa"].str.contains(r"POAAR|POAR", case=False, na=False).map({True: "SI", False: "NO"})

    logging.info("Cargando catálogos...")
    cp_df = pd.read_excel(cfg.BASE_PATH / cfg.CULTIVOS_PRIORIZADOS_FILE, sheet_name="cultivos")
    cp_df2 = pd.read_excel(cfg.BASE_PATH / cfg.CULTIVOS_PRIORIZADOS2_FILE, sheet_name="cultivos")

    cultivos_priorizados = cp_df["cultivo_priorizado"].dropna().str.upper().unique().tolist()
    cultivos_priorizados2 = cp_df2["cultivo_priorizado"].dropna().str.upper().unique().tolist()

    proyectos_integrales = pd.read_excel(cfg.BASE_PATH / cfg.INTEGRALES_FILE, sheet_name="integrales")
    proyectos_integrales = proyectos_integrales["proyecto"].dropna().str.upper().unique().tolist()

    replacements_df = pd.read_excel(cfg.BASE_PATH / cfg.REPLACEMENTS_FILE, sheet_name="reemplazos")
    replacements = dict(zip(replacements_df["original"].str.upper(), replacements_df["estandarizado"].str.upper()))

    logging.info("Aplicando priorización de cultivos...")
    df = processor.aplicar_priorizacion_cultivos(df, cultivos_priorizados, cultivos_priorizados2, replacements)
    df = processor.aplicar_proyectos_integrales(df, proyectos_integrales)

    df["ubigeo"] = DataUtils.crear_ubigeo(df)
    df = df.merge(df_dp[["ubigeo", "es_distrtito_poaar"]], on="ubigeo", how="left")

    logging.info("Validando cultivos y crianzas...")
    df_tv = DataUtils.cargar_excel(cfg.BASE_PATH / cfg.CULTIVOS_VALIDACION_FILE, sheet_name="tb_validar")
    df_tv["ubigeo"] = df_tv["ubigeo"].astype(str).str.zfill(6)

    df["key"] = df["cultivo_priorizado"] + df["ubigeo"]
    df_tv["key"] = df_tv["cultivo"] + df_tv["ubigeo"]
    df_tv["en_distrito_y_cultivo"] = "SI"

    df = df.merge(df_tv[["key", "en_distrito_y_cultivo", "tipo_ccf", "categoria_ccf", "es_vraem"]],
                  on="key", how="left")

    df["cultivo_priorizado"] = df.apply(
        lambda row: f"TRANSVERSAL {row['tipo_ccf']}" if row["categoria_ccf"] == "SOPORTE PRODUCTIVO" else row["cultivo_priorizado"],
        axis=1
    )

    df = df.drop_duplicates()
    df = processor.marcar_articulados(df)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = cfg.EXPORT_PATH / f"df_final_{timestamp}.csv"
    df.to_csv(output_file, index=False, sep=",", quoting=1, quotechar='"', encoding="utf-8-sig")

    logging.info(f"Archivo exportado con éxito: {output_file}")

# =======================
# EJECUCIÓN
# =======================
if __name__ == "__main__":
    main()
