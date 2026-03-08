import streamlit as st
import requests
import time

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Búnker RADnet", 
    page_icon="☢️", 
    layout="wide"
)

# Título principal del Laboratorio
st.title("☢️ Panel de Monitoreo - Manu Laboratorio")
st.markdown("---")

# URL de tu implementación de Google Apps Script (Puente)
URL_API = "https://script.google.com/macros/s/AKfycbwZfsaIFSmssXIo_7u_TKpwjuBl2WcI0VWdQOQRFyTrpxYfaPGTZq3z4B_XMrJ5sEGK/exec"

# ==========================================
# 2. FUNCIONES DE COMUNICACIÓN
# ==========================================

def obtener_datos(tiempo_espera=3):
    """Obtiene los datos en formato JSON desde Google Apps Script."""
    try:
        r = requests.get(URL_API, timeout=tiempo_espera)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

# ==========================================
# 3. BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("⚙️ Control de Enlace")
    st.write("Presiona para forzar una sincronización inmediata con el ESP32.")
    
    if st.button('🔄 Sincronizar con el Laboratorio'):
        with st.status("Verificando conexión...", expanded=False) as status:
            # Petición manual con mayor margen de tiempo
            prueba_datos = obtener_datos(tiempo_espera=10)
            if prueba_datos:
                status.update(label="¡Sincronización Exitosa!", state="complete", expanded=False)
                if prueba_datos['conexion'] == "EN LÍNEA":
                    st.success("Sistema Conectado")
                else:
                    st.warning("Sistema Registrado (Fuera de Línea)")
            else:
                status.update(label="Error de conexión", state="error", expanded=False)
                st.error("El puente no respondió.")
    
    st.divider()
    st.info("""
    **INFO DEL SISTEMA:**
    - El ESP32 envía datos cada 45s (Heartbeat).
    - El panel se refresca solo cada 5s.
    """)

# ==========================================
# 4. MONITOR EN TIEMPO REAL (Lógica Principal)
# ==========================================

# Contenedor dinámico que se limpia y actualiza en cada ciclo
placeholder = st.empty()

while True:
    datos = obtener_datos()
    
    with placeholder.container():
        if datos:
            # A. Indicador de Conexión del ESP32
            if datos['conexion'] == "EN LÍNEA":
                st.success(f"● SISTEMA EN LÍNEA (Última señal hace instantes)")
            else:
                st.error(f"○ SISTEMA FUERA DE LÍNEA (El ESP32 no ha enviado señal recientemente)")

            st.write("") # Espaciador

            # B. Estado Actual y Hora
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Estado del LED")
                color = "green" if datos['estado'] == "ENCENDIDO" else "red"
                st.markdown(f"""
                    <div style='background-color: rgba(0,0,0,0.1); padding: 20px; border-radius: 10px; border-left: 5px solid {color};'>
                        <h1 style='color:{color}; margin: 0;'>{datos['estado']}</h1>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("Última Acción Registrada")
                st.info(f"📅 {datos['fecha']}")

            st.divider()

            # C. Tabla de Historial (Novedad)
            st.subheader("📝 Historial de Estados (Últimos 5 cambios)")
            if datos.get('historial') and len(datos['historial']) > 0:
                st.table(datos['historial'])
            else:
                st.write("No hay eventos recientes registrados.")

        else:
            # Mensaje en caso de falla temporal de red en la web
            st.warning("⚠️ Esperando respuesta del servidor de Google... Reintentando automáticamente.")

    # Pausa obligatoria del bucle para no saturar la API
    time.sleep(5)
