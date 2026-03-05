import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. Configuración de la interfaz
st.set_page_config(page_title="Búnker RADnet", page_icon="☢️")

st.title("☢️ Panel de Control - Búnker RADnet")
st.write("Interfaz web para monitorear y enviar señales al sistema.")

# 2. URL de tu Google Apps Script (Tu "Búnker")
# Asegúrate de que esta URL sea la más reciente de tu implementación
URL_BUNKER = "https://script.google.com/macros/s/AKfycbwJpT5-Sw2w65G1zcyUIrRhmZVdZwLWk5x5CrzQ2gYyTmsR0raouhpYqKS1zHwWFM7lYg/exec"

# 3. Formulario lateral para enviar datos manualmente
st.sidebar.header("Simulador de Nodo")
nodo = st.sidebar.selectbox("Seleccionar Nodo", ["MANUEL_LAB", "ESP32_PROTOTIPO", "NODO_EXTERNO"])
sensor = st.sidebar.text_input("Sensor", "CONEXION")
valor = st.sidebar.slider("Valor de señal", 0, 100, 1)
estado = st.sidebar.radio("Estado", ["ACTIVO", "ALERTA", "MANTENIMIENTO"])

if st.sidebar.button("🚀 Enviar a la Nube"):
    # Preparamos el paquete JSON
    datos = {
        "nodo": nodo,
        "sensor": sensor,
        "valor": valor,
        "estado": estado
    }
    
    try:
        # Enviamos la petición POST
        res = requests.post(URL_BUNKER, json=datos, timeout=10)
        
        if res.status_code == 200:
            st.sidebar.success(f"✅ ¡Señal enviada! Respuesta: {res.text}")
        else:
            st.sidebar.error(f"❌ Error {res.status_code}")
    except Exception as e:
        st.sidebar.error(f"❌ No se pudo conectar: {e}")

# 4. Visualización de datos (Simulación de monitoreo)
st.subheader("Estado Actual del Sistema")
col1, col2, col3 = st.columns(3)

col1.metric("Nodo Activo", nodo)
col2.metric("Último Valor", f"{valor}%")
col3.metric("Conectividad", "Excelente", "120ms")

# Tabla decorativa para ver el historial de lo que estamos configurando
st.info("Nota: Los datos enviados aparecerán en tu Google Sheet configurada.")
df = pd.DataFrame([datos] if 'datos' in locals() else [])
if not df.empty:
    st.write("Último paquete configurado:")
    st.table(df)
