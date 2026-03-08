import streamlit as st
import requests
import time

# ... (Configuración inicial y URL_API)

def obtener_datos():
    try:
        # Aumentamos el timeout para asegurar la sincronización manual
        r = requests.get(URL_API, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# Sidebar o Panel Principal para el botón de sincronización
with st.sidebar:
    st.header("Control de Enlace")
    if st.button('🔄 Sincronizar ESP32 con Web'):
        with st.spinner('Verificando conexión con el laboratorio...'):
            datos_manuales = obtener_datos()
            if datos_manuales:
                st.success("Sincronización Exitosa")
                # Forzamos el refresco de los valores globales
                st.session_state.last_sync = datos_manuales
            else:
                st.error("No se pudo establecer el enlace")

# El resto de tu lógica de visualización usará st.session_state.last_sync
