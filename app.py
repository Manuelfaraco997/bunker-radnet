import streamlit as st
import pandas as pd
import time

# Configuración visual
st.set_page_config(page_title="Laboratorio", page_icon="☢️", layout="wide")

st.title("☢️ Panel de Monitoreo - Manu Laboratorio")
st.write("Datos recibidos en tiempo real desde el ESP32")

# --- CONEXIÓN CON LA BASE DE DATOS (Google Sheets) ---
# 1. Ve a tu hoja de cálculo, haz clic en 'Archivo' > 'Compartir' > 'Publicar en la web'
# 2. Selecciona 'Valores separados por comas (.csv)' y copia ese link aquí:
CSV_URL = "https://docs.google.com/spreadsheets/d/TU_ID_AQUI/export?format=csv"

def cargar_datos():
    # El parámetro 'clear_cache' evita que Streamlit guarde datos viejos
    return pd.read_csv(CSV_URL)

# Botón de actualización manual
if st.button('🔄 Sincronizar con el Laboratorio'):
    try:
        df = cargar_datos()
        
        # Último registro enviado por el ESP32
        ultimo = df.iloc[-1]
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Último Nodo", ultimo['nodo'])
        col2.metric("Sensor", ultimo['sensor'])
        col3.metric("Valor Actual", f"{ultimo['valor']}")
        col4.metric("Estado", ultimo['estado'])

        # Gráfica de historial
        st.subheader("📈 Historial de Señales")
        st.line_chart(df['valor'])

        # Tabla de datos crudos
        with st.expander("Ver tabla de registros completa"):
            st.dataframe(df.sort_index(ascending=False))
            
    except Exception as e:
        st.error(f"Esperando datos del ESP32... Error: {e}")

st.sidebar.markdown("### Configuración del Sistema")
st.sidebar.info("El ESP32 envía datos mediante el código de Arduino IDE a través de Google Apps Script.")
