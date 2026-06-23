# ============================================================
# Script 03 - Procesamiento y Creación de Variables
# Proyecto: Human Behavior AI
# BD-141 Big Data — CUC — Cuatrimestre II 2026
# ============================================================

import pandas as pd
import sqlite3
from datetime import datetime

def crear_variables(df):
    """
    Crea variables de comportamiento a partir del dataset limpio.
    """
    print("=== CREACION DE VARIABLES ===")

    df = df.copy()

    # Variables temporales
    df['anio_creacion'] = df['Created At'].dt.year
    df['mes_creacion']  = df['Created At'].dt.month
    df['hora_creacion'] = df['Created At'].dt.hour
    df['dia_semana']    = df['Created At'].dt.dayofweek

    # Franja horaria
    def franja_horaria(hora):
        if 0 <= hora < 6:
            return 'madrugada'
        elif 6 <= hora < 12:
            return 'mañana'
        elif 12 <= hora < 18:
            return 'tarde'
        else:
            return 'noche'

    df['franja_horaria']    = df['hora_creacion'].apply(franja_horaria)
    df['es_fin_de_semana']  = df['dia_semana'].apply(lambda x: 1 if x >= 5 else 0)

    fecha_ref = df['Created At'].max()
    df['antiguedad_dias'] = (fecha_ref - df['Created At']).dt.days

    # Variables de actividad
    df['engagement_ratio']       = ((df['Retweet Count'] + df['Mention Count']) / (df['Follower Count'] + 1)).round(4)
    df['actividad_total']        = df['Retweet Count'] + df['Mention Count']
    df['ratio_retweet_mencion']  = (df['Retweet Count'] / (df['Mention Count'] + 1)).round(4)
    df['verificado_int']         = df['Verified'].astype(int)

    # Variables de contenido
    df['cantidad_hashtags'] = df['Hashtags'].apply(lambda x: 0 if x == 'sin_hashtags' else len(str(x).split()))
    df['largo_tweet']       = df['Tweet'].astype(str).apply(len)
    df['palabras_tweet']    = df['Tweet'].astype(str).apply(lambda x: len(x.split()))
    df['usa_hashtags']      = df['cantidad_hashtags'].apply(lambda x: 1 if x > 0 else 0)

    # Variables de riesgo
    df['alta_actividad_pocos_seguidores'] = (
        (df['Follower Count'] < df['Follower Count'].quantile(0.25)) &
        (df['actividad_total'] > df['actividad_total'].quantile(0.75))
    ).astype(int)

    df['no_verif_alto_engagement'] = (
        (df['verificado_int'] == 0) &
        (df['engagement_ratio'] > df['engagement_ratio'].quantile(0.90))
    ).astype(int)

    df['activo_madrugada'] = (df['franja_horaria'] == 'madrugada').astype(int)
    df['score_sospecha']   = df['alta_actividad_pocos_seguidores'] + df['no_verif_alto_engagement'] + df['activo_madrugada']

    print(f"Variables creadas exitosamente")
    print(f"Dataset procesado: {df.shape[0]:,} filas x {df.shape[1]} columnas")

    return df


def cargar_a_sqlite(df_raw, df_procesado, db='humanbehaviorai.db'):
    """
    Carga los datos en las tablas raw_events y processed_sessions.
    """
    print("\n=== CARGA A SQLITE ===")

    conn = sqlite3.connect(db)

    # Cargar raw_events
    df_raw.rename(columns={
        'User ID': 'user_id', 'Username': 'username', 'Tweet': 'tweet',
        'Retweet Count': 'retweet_count', 'Mention Count': 'mention_count',
        'Follower Count': 'follower_count', 'Verified': 'verified',
        'Bot Label': 'bot_label', 'Location': 'location',
        'Created At': 'created_at', 'Hashtags': 'hashtags'
    }, inplace=False).to_sql('raw_events', conn, if_exists='replace', index=False)
    print(f"raw_events cargada: {len(df_raw):,} registros")

    # Cargar processed_sessions
    columnas = [
        'User ID', 'engagement_ratio', 'actividad_total', 'ratio_retweet_mencion',
        'franja_horaria', 'es_fin_de_semana', 'antiguedad_dias',
        'cantidad_hashtags', 'largo_tweet', 'palabras_tweet',
        'usa_hashtags', 'score_sospecha', 'Bot Label'
    ]
    df_proc = df_procesado[columnas].copy()
    df_proc.columns = [
        'user_id', 'engagement_ratio', 'actividad_total', 'ratio_retweet_mencion',
        'franja_horaria', 'es_fin_de_semana', 'antiguedad_dias',
        'cantidad_hashtags', 'largo_tweet', 'palabras_tweet',
        'usa_hashtags', 'score_sospecha', 'bot_label'
    ]
    df_proc['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df_proc.to_sql('processed_sessions', conn, if_exists='replace', index=False)
    print(f"processed_sessions cargada: {len(df_proc):,} registros")

    conn.close()
    print("Carga completada y conexion cerrada")


if __name__ == "__main__":
    from script_01_carga import cargar_dataset
    from script_02_limpieza import limpiar_dataset
    df_raw    = cargar_dataset()
    df_limpio = limpiar_dataset(df_raw)
    df_proc   = crear_variables(df_limpio)
    cargar_a_sqlite(df_raw, df_proc)