import streamlit as st
import pandas as pd
import os

# ==========================================================
# Human Behavior AI — Dashboard de resultados
# BD-141 Big Data — CUC — Cuatrimestre II 2026
#
# Este dashboard NO reentrena ningún modelo ni corre pipelines
# en vivo. Solo muestra los resultados que los notebooks de
# cada fase ya generaron (imágenes .png y el CSV procesado).
# ==========================================================

st.set_page_config(
    page_title="Human Behavior AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

RUTA_IMAGENES = "notebooks"
RUTA_CSV = os.path.join("data", "processed", "bot_detection_procesado.csv")

st.title("🤖 Human Behavior AI")
st.subheader("Detección de Manipulación Digital y Comportamiento Artificial")
st.caption("BD-141 Big Data · Colegio Universitario de Cartago · Profesora Ericka Valverde Navarro · II Cuatrimestre 2026")
st.caption("Equipo: Mariana Méndez Pérez · Luis Diego Montero Vargas · Josué Redondo Gómez · Claret Rodríguez Jiménez · Nadin Rojas López")

st.divider()


def mostrar_imagen(nombre_archivo, descripcion=""):
    """Muestra una imagen de la carpeta notebooks si existe, o un aviso si falta."""
    ruta = os.path.join(RUTA_IMAGENES, nombre_archivo)
    if os.path.exists(ruta):
        st.image(ruta, use_container_width=True)
        if descripcion:
            st.caption(descripcion)
    else:
        st.warning(f"No se encontró la imagen: {nombre_archivo}")


tab_resumen, tab_eda, tab_modelo, tab_pipeline, tab_nube, tab_datos = st.tabs(
    ["Resumen", "Análisis (Fase 3-4)", "Modelo de IA (Fase 4)",
     "Pipeline (Fase 5)", "Nube y Riesgos (Fase 6)", "Explorar Dataset"]
)

# ---------------------------------------------------------
with tab_resumen:
    st.header("Resumen del proyecto")
    st.markdown("""
    Este sistema intenta detectar si una cuenta de Twitter/X es un **bot** (cuenta
    automatizada) o un **humano real**, analizando su comportamiento: retweets,
    menciones, seguidores, horarios de actividad, y patrones de contenido.
    """)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros analizados", "50,000")
    col2.metric("Variables procesadas", "30")
    col3.metric("Registros integrados (Fase 5)", "53,500")
    col4.metric("Accuracy del modelo", "~49.5%")

    st.info(
        " **Hallazgo central del proyecto:** el análisis exploratorio (Fase 4) "
        "demostró que ninguna variable de comportamiento disponible separa realmente "
        "cuentas bot de humanas en este dataset (correlación máxima con la etiqueta: "
        "0.0069). Dos modelos con lógicas distintas — Random Forest e Isolation Forest — "
        "llegan al mismo techo de ~50% de accuracy, equivalente al azar. Esto se explica "
        "porque el dataset original parece estar generado de forma sintética, sin conectar "
        "el comportamiento real con la etiqueta de bot."
    )

# ---------------------------------------------------------
with tab_eda:
    st.header("Análisis exploratorio y hallazgos (Fase 3 y 4)")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Calidad de los datos**")
        mostrar_imagen("nulos_por_columna.png", "Revisión de valores nulos por columna")
    with c2:
        st.markdown("**Balance de clases**")
        mostrar_imagen("distribucion_clases.png", "Distribución de cuentas Bot vs Humano")

    st.markdown("**Distribución de variables numéricas**")
    mostrar_imagen("distribucion_variables_numericas.png")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Actividad por franja horaria**")
        mostrar_imagen("actividad_franja_horaria.png")
    with c4:
        st.markdown("**Engagement ratio sin outliers**")
        mostrar_imagen("engagement_sin_outliers.png",
                        "Al quitar valores extremos, las distribuciones de bot y humano quedan casi idénticas")

    st.markdown("**Matriz de correlación**")
    mostrar_imagen("mapa_correlacion.png",
                    "La fila de Bot Label no muestra ninguna correlación relevante con las demás variables")

# ---------------------------------------------------------
with tab_modelo:
    st.header("Modelo de IA preliminar (Fase 4)")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Matriz de confusión — Random Forest**")
        mostrar_imagen("matriz_confusion.png")
    with c2:
        st.markdown("**Matriz de confusión — Isolation Forest**")
        mostrar_imagen("matriz_confusion_if.png")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Comparación de modelos**")
        mostrar_imagen("comparacion_modelos.png")
    with c4:
        st.markdown("**Importancia de variables**")
        mostrar_imagen("importancia_variables.png")

    st.warning(
        "Ambos modelos rondan el 50% de accuracy — el mismo desempeño que adivinar al "
        "azar. Esto no es un error de implementación: refleja la ausencia de señal real "
        "en las variables disponibles, confirmada en el análisis exploratorio."
    )

# ---------------------------------------------------------
with tab_pipeline:
    st.header("Integración y automatización (Fase 5)")

    st.markdown("**Integración de múltiples fuentes de datos**")
    mostrar_imagen("integracion_fuentes.png",
                    "Base histórica (Kaggle, 50,000) + Twitter simulado (2,000) + Reddit simulado (1,500) = 53,500 registros")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Simulación de datos en tiempo real**")
        mostrar_imagen("simulacion_tiempo_real.png", "5 lotes de 200 registros, procesados en menos de 0.05s cada uno")
    with c2:
        st.markdown("**Flujo completo del pipeline**")
        mostrar_imagen("flujo_completo.png")

    st.markdown("**Resultados del pipeline automatizado**")
    mostrar_imagen("resultados_pipeline.png")

# ---------------------------------------------------------
with tab_nube:
    st.header("Escalabilidad, nube y optimización (Fase 6)")

    st.markdown("**Escalabilidad por tecnología**")
    mostrar_imagen("escalabilidad.png",
                    "Python + Pandas colapsa a partir de 50M de registros; Spark y Kafka+Spark sí escalan")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Arquitectura propuesta en la nube (GCP)**")
        mostrar_imagen("arquitectura_cloud.png")
    with c2:
        st.markdown("**Matriz de riesgos del sistema**")
        mostrar_imagen("mapa_riesgos.png")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Costos aproximados**")
        mostrar_imagen("costos_gcp.png", "Diseño inicial: ~$559 USD/mes → Optimizado: ~$164 USD/mes")
    with c4:
        st.markdown("**Roadmap de optimización**")
        mostrar_imagen("roadmap_optimizacion.png")

# ---------------------------------------------------------
with tab_datos:
    st.header("Explorar el dataset procesado")

    if os.path.exists(RUTA_CSV):
        df = pd.read_csv(RUTA_CSV)

        col1, col2 = st.columns(2)
        with col1:
            filtro_bot = st.selectbox("Filtrar por tipo de cuenta", ["Todas", "Solo Bots (1)", "Solo Humanos (0)"])
        with col2:
            n_filas = st.slider("Cantidad de filas a mostrar", 10, 200, 50)

        df_filtrado = df.copy()
        if filtro_bot == "Solo Bots (1)":
            df_filtrado = df_filtrado[df_filtrado["Bot Label"] == 1]
        elif filtro_bot == "Solo Humanos (0)":
            df_filtrado = df_filtrado[df_filtrado["Bot Label"] == 0]

        st.write(f"Mostrando {min(n_filas, len(df_filtrado))} de {len(df_filtrado):,} registros filtrados "
                 f"(dataset completo: {len(df):,} filas, {df.shape[1]} columnas)")
        st.dataframe(df_filtrado.head(n_filas), use_container_width=True)

        st.markdown("**Estadísticas descriptivas**")
        st.dataframe(df_filtrado.describe(), use_container_width=True)
    else:
        st.error(
            f"No se encontró el archivo en '{RUTA_CSV}'. "
            "Corre este dashboard desde la carpeta raíz del repositorio (HumanBehaviorAI/), "
            "no desde dentro de 'notebooks/'."
        )

st.divider()
st.caption("Dashboard construido con Streamlit — muestra resultados generados por los notebooks de las Fases 3 a 6.")
