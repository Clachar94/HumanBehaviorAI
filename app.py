import streamlit as st
import pandas as pd
import os

# ==========================================================
# Human Behavior AI — Dashboard organizado por fases
# BD-141 Big Data — CUC — Cuatrimestre II 2026
#
# Este dashboard NO reentrena modelos ni corre pipelines en
# vivo. Muestra los resultados que los notebooks de cada fase
# ya generaron, organizados igual que la presentación.
# ==========================================================

st.set_page_config(page_title="Human Behavior AI", layout="wide", initial_sidebar_state="collapsed")

RUTA_IMAGENES = "notebooks"
RUTA_CSV = os.path.join("data", "processed", "bot_detection_procesado.csv")

st.title("Human Behavior AI")
st.subheader("Detección de Manipulación Digital y Comportamiento Artificial")
st.caption("BD-141 Big Data · Colegio Universitario de Cartago · Profesora Ericka Valverde Navarro · II Cuatrimestre 2026")
st.caption("Equipo: Mariana Méndez Pérez · Luis Diego Montero Vargas · Josué Redondo Gómez · Claret Rodríguez Jiménez · Nadin Rojas López")
st.divider()


def imagen(nombre, caption=""):
    ruta = os.path.join(RUTA_IMAGENES, nombre)
    if os.path.exists(ruta):
        st.image(ruta, use_container_width=True, caption=caption)
    else:
        st.info(f"Imagen no disponible en esta copia local: {nombre}")


tabs = st.tabs([
    "Resumen",
    "Fase 1-2 · Problema y Arquitectura",
    "Fase 3 · Procesamiento",
    "Fase 4 · Análisis e IA",
    "Fase 5 · Integración",
    "Fase 6 · Escalabilidad",
    "Explorar Datos",
])

# ---------------------------------------------------------
with tabs[0]:
    st.header("Resumen del proyecto")
    st.markdown(
        "Este sistema intenta detectar si una cuenta de Twitter/X es un **bot** o un **humano real**, "
        "analizando su comportamiento: retweets, seguidores, horarios y patrones de contenido."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registros analizados", "50,000")
    c2.metric("Variables procesadas", "30")
    c3.metric("Registros integrados (Fase 5)", "53,500")
    c4.metric("Accuracy del modelo", "~49.5%")
    st.info(
        "**Hallazgo central:** ninguna variable de comportamiento disponible separa realmente cuentas bot "
        "de humanas en este dataset (correlación máxima con la etiqueta: 0.0069). Dos modelos con lógicas "
        "distintas —Random Forest e Isolation Forest— llegan al mismo techo de ~50% de accuracy, equivalente "
        "al azar. Esto se explica en detalle en la pestaña de Fase 4."
    )
    st.markdown("**Navegación:** cada pestaña de arriba corresponde a una fase del proyecto, en el mismo orden que la presentación.")

# ---------------------------------------------------------
with tabs[1]:
    st.header("Fase 1-2 · El problema y la arquitectura")
    st.markdown("""
    **El problema:** los bots simulan ser humanos en redes sociales, manipulando métricas como likes,
    comentarios y tendencias. Esto genera pérdidas estimadas de **$100,000 millones de dólares al año**
    en fraude publicitario digital.

    **La arquitectura propuesta**, en 5 capas:
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        1. **Ingesta** — datasets de Kaggle + datos simulados
        2. **Almacenamiento** — PostgreSQL (raw_events, processed_sessions)
        3. **Procesamiento** — Python + Pandas
        """)
    with col2:
        st.markdown("""
        4. **Inteligencia Artificial** — Scikit-Learn (Random Forest + Isolation Forest)
        5. **Visualización** — Streamlit (este dashboard)
        """)
    st.caption("Esta fase no genera gráficos de datos — es la etapa de definición y diseño del proyecto.")

# ---------------------------------------------------------
with tabs[2]:
    st.header("Fase 3 · Procesamiento de datos")
    st.markdown(
        "Se limpiaron 8,341 valores nulos, se corrigieron formatos de fecha, y se crearon **19 variables "
        "nuevas** a partir de las 11 originales, organizadas en 4 categorías: actividad, temporales, "
        "contenido y riesgo. El dataset pasó de 11 a 30 columnas, con 0 valores nulos."
    )
    st.markdown("**Confirmación visual de que la limpieza funcionó — cero valores nulos en todas las columnas:**")
    imagen("nulos_por_columna.png", "Revisión de valores nulos por columna, después de la limpieza")
    st.success(
        "Además, se ejecutaron 4 consultas SQL reales sobre la base de datos (conteo por tipo de cuenta, "
        "engagement promedio, top 5 de sospecha, actividad de madrugada) — disponibles en el notebook Fase3.ipynb, sección 8."
    )

# ---------------------------------------------------------
with tabs[3]:
    st.header("Fase 4 · Análisis e Inteligencia Artificial")
    st.markdown(
        "Se entrenaron dos modelos para detectar bots. **Ninguno logró superar el 50% de accuracy** — "
        "el mismo resultado que adivinar al azar."
    )
    c1, c2 = st.columns(2)
    c1.metric("Random Forest", "49.54%", help="Modelo supervisado, 100 árboles")
    c2.metric("Isolation Forest", "49.40%", help="Modelo no supervisado, detección de anomalías")

    st.markdown("**¿Por qué pasa esto? Este mapa de correlación lo muestra:**")
    imagen("mapa_correlacion.png",
           "La fila de 'Bot Label' aparece vacía: ninguna variable alcanza una correlación relevante con ella")
    st.warning(
        "La correlación más alta encontrada entre cualquier variable y la etiqueta de bot fue de apenas "
        "**0.0069** — en una escala de 0 a 1, prácticamente cero. Esto confirma que el dataset no contiene "
        "la información necesaria para distinguir bots de humanos, sin importar qué tan bueno sea el modelo."
    )

# ---------------------------------------------------------
with tabs[4]:
    st.header("Fase 5 · Integración y Automatización")
    st.markdown(
        "Se combinaron 3 fuentes de datos (Kaggle, Twitter simulado, Reddit simulado) en un solo dataset "
        "de **53,500 registros**, y se construyó un pipeline automatizado de 7 etapas que procesa datos "
        "en tiempo real."
    )
    imagen("flujo_completo.png", "Las 7 etapas del pipeline automatizado, de principio a fin")
    st.markdown(
        "El pipeline es de tipo **síncrono**: cada etapa espera a que la anterior termine, ya que depende "
        "de su resultado. Procesa lotes de 200 registros en menos de 0.05 segundos cada uno."
    )

# ---------------------------------------------------------
with tabs[5]:
    st.header("Fase 6 · Escalabilidad, Nube y Optimización")
    st.markdown(
        "Se diseñó cómo el sistema crecería en producción real, migrando a Google Cloud Platform con "
        "Apache Spark y Kafka para manejar millones de registros."
    )
    imagen("escalabilidad.png",
           "Python + Pandas (actual) colapsa a partir de 50M de registros; Spark y Kafka+Spark sí escalan")
    c1, c2 = st.columns(2)
    c1.metric("Costo inicial estimado", "~$559 USD/mes")
    c2.metric("Costo optimizado", "~$164 USD/mes", delta="-70%", delta_color="normal")
    st.caption("Optimización lograda sustituyendo Cloud Composer por Cloud Scheduler para tareas de orquestación simples.")

# ---------------------------------------------------------
with tabs[6]:
    st.header("Explorar el dataset procesado")
    if os.path.exists(RUTA_CSV):
        df = pd.read_csv(RUTA_CSV)
        col1, col2 = st.columns(2)
        with col1:
            filtro = st.selectbox("Filtrar por tipo de cuenta", ["Todas", "Solo Bots (1)", "Solo Humanos (0)"])
        with col2:
            n_filas = st.slider("Filas a mostrar", 10, 200, 50)

        df_filtrado = df.copy()
        if filtro == "Solo Bots (1)":
            df_filtrado = df_filtrado[df_filtrado["Bot Label"] == 1]
        elif filtro == "Solo Humanos (0)":
            df_filtrado = df_filtrado[df_filtrado["Bot Label"] == 0]

        st.write(f"Mostrando {min(n_filas, len(df_filtrado))} de {len(df_filtrado):,} registros filtrados "
                 f"(dataset completo: {len(df):,} filas, {df.shape[1]} columnas)")
        st.dataframe(df_filtrado.head(n_filas), use_container_width=True)
    else:
        st.error(f"No se encontró '{RUTA_CSV}'. Corre este dashboard desde la carpeta raíz del repositorio.")

st.divider()
st.caption("Dashboard construido con Streamlit — organizado por las 6 fases del proyecto Human Behavior AI.")
