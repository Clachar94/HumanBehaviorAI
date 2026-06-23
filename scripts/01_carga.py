# ============================================================
# Script 01 - Carga del Dataset
# Proyecto: Human Behavior AI
# BD-141 Big Data — CUC — Cuatrimestre II 2026
# ============================================================

import pandas as pd
import os

def cargar_dataset(ruta='bot_detection_data.csv'):
    """
    Carga el dataset original y muestra información general.
    """
    print("=== CARGA DEL DATASET ===")
    
    if not os.path.exists(ruta):
        print(f"Error: No se encontró el archivo {ruta}")
        return None
    
    df = pd.read_csv(ruta)
    
    print(f"Archivo cargado: {ruta}")
    print(f"Filas:           {df.shape[0]:,}")
    print(f"Columnas:        {df.shape[1]}")
    print(f"\nColumnas disponibles:")
    for col in df.columns:
        print(f"  - {col} ({df[col].dtype})")
    
    print(f"\nValores nulos por columna:")
    print(df.isnull().sum())
    
    return df

if __name__ == "__main__":
    df = cargar_dataset()