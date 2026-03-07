import streamlit as st
import requests
import time

st.set_page_config(page_title="Búnker RADnet", page_icon="☢️", layout="wide")

st.title("☢️ Panel de Monitoreo - Manu Laboratorio")

URL_API = "https://script.google.com/macros/s/AKfycbz1HZHcNLR7xXMFxkgQAIJXJhz14R0c7npKqdE8xuMUbQPljZURyDIyI0yWHtdqNQYnFw/exec"

def obtener_datos():
    try:
        r = requests.get(URL_API, timeout=3)
        return r.json()
    except:
        return None

# Contenedor dinámico
placeholder = st.empty()

while True:
    datos = obtener_datos()
    with placeholder.container():
        if datos:
            # Cabecera de Conexión
            if datos['conexion'] == "EN LÍNEA":
                st.success("● SISTEMA EN LÍNEA (ESP32 Conectado)")
            else:
                st.error("○ SISTEMA FUERA DE LÍNEA (Sin señal del ESP32)")

            st.divider()
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("Estado del LED")
                color = "green" if datos['estado'] == "ENCENDIDO" else "red"
                st.markdown(f"<h1 style='color:{color};'>{datos['estado']}</h1>", unsafe_allow_html=True)
            
            with c2:
                st.subheader("Última Acción Registrada")
                st.info(f"📅 {datos['fecha']}")
        else:
            st.warning("⚠️ No se puede conectar con el puente de Google...")

    time.sleep(5) # Auto-actualización cada 5 segundos
