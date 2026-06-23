# ============================================================
# Script 02 - Limpieza de Datos
# Proyecto: Human Behavior AI
# BD-141 Big Data — CUC — Cuatrimestre II 2026
# ============================================================

import pandas as pd

def limpiar_dataset(df):
    """
    Aplica limpieza al dataset: nulos, duplicados y formatos.
    """
    print("=== LIMPIEZA DE DATOS ===")
    
    df = df.copy()
    
    # Tratamiento de nulos en Hashtags
    nulos_antes = df['Hashtags'].isnull().sum()
    df['Hashtags'] = df['Hashtags'].fillna('sin_hashtags')
    print(f"Nulos en Hashtags tratados: {nulos_antes:,} → 0")
    
    # Eliminar duplicados
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        df = df.drop_duplicates()
        print(f"Duplicados eliminados: {duplicados:,}")
    else:
        print("Sin duplicados encontrados")
    
    # Convertir Created At a datetime
    df['Created At'] = pd.to_datetime(df['Created At'])
    print("Created At convertido a datetime")
    
    # Estandarizar texto
    df['Location'] = df['Location'].str.strip().str.title()
    df['Hashtags'] = df['Hashtags'].str.strip().str.lower()
    print("Columnas de texto estandarizadas")
    
    print(f"\nDataset limpio: {df.shape[0]:,} filas x {df.shape[1]} columnas")
    print(f"Nulos restantes: {df.isnull().sum().sum()}")
    
    return df

if __name__ == "__main__":
    from script_01_carga import cargar_dataset
    df_raw = cargar_dataset()
    df_limpio = limpiar_dataset(df_raw)