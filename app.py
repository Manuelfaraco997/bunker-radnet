import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Panel de Monitoreo - Manu", page_icon="☢️")

st.title("☢️ Panel de Monitoreo - Manu Laboratorio")
st.markdown("Datos recibidos en tiempo real desde el ESP32 a través de Google Apps Script.")

# --- CAMBIA ESTA URL POR LA QUE COPIASTE DE GOOGLE ---
URL_API = "https://script.google.com/macros/s/AKfycbwahQzl73Lcx1ZGtmCdHXgYk1QE1ab0HTl3ZlE1opeiuLnbK-aLnpk77UpvJMdqdoWTdA/exec"

def obtener_datos():
    try:
        # Añadimos un timeout para evitar que la app se quede colgada
        response = requests.get(URL_API, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return {"error": str(e)}

# Interfaz de usuario
if st.button('🔄 Sincronizar con el Laboratorio'):
    with st.spinner('Consultando al ESP32...'):
        datos = obtener_datos()
        
    if datos and "error" not in datos:
        st.success("¡Sincronización exitosa!")
        col1, col2 = st.columns(2)
        
        # Estilo visual para el estado
        estado = datos['estado']
        color = "green" if estado == "ENCENDIDO" else "red"
        
        col1.markdown(f"### Estado del LED\n# <span style='color:{color}'>{estado}</span>", unsafe_allow_html=True)
        col2.metric("Última Actualización", datos['fecha'])
    else:
        st.error(f"Error de conexión: {datos.get('error', 'No se encontró la API (404)')}")

st.divider()
st.sidebar.title("Configuración")
st.sidebar.info("El ESP32 envía datos mediante el código de Arduino IDE a través de Google Apps Script.")
