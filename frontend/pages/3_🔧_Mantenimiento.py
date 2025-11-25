import streamlit as st
import requests
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Gestión de Mantenimiento", page_icon="🔧", layout="wide")

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

st.title("🔧 Gestión de Mantenimiento")
st.markdown("---")

# Funciones auxiliares para obtener datos
def get_mantenimientos():
    try:
        # Nota: La ruta depende de cómo definimos el proxy en el API Gateway
        # En el paso 4.1 mapeamos /api/mantenimientos -> mantenimiento-service
        response = requests.get(f"{API_URL}/api/mantenimientos", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_equipos_simple():
    try:
        response = requests.get(f"{API_URL}/api/equipos", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

# Cargar datos iniciales
mantenimientos = get_mantenimientos()
equipos = get_equipos_simple()

# Crear diccionario para mapear ID de equipo a Nombre rápidamente
equipos_dict = {e['id']: f"{e['codigo_inventario']} - {e['nombre']}" for e in equipos} if equipos else {}

tab1, tab2 = st.tabs(["📅 Calendario y Lista", "➕ Programar Mantenimiento"])

# --- TAB 1: LISTADO ---
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Historial y Programación")
    with col2:
        if st.button("🔄 Actualizar", use_container_width=True):
            st.rerun()

    if mantenimientos:
        df = pd.DataFrame(mantenimientos)
        
        # Enriquecer el DF con el nombre del equipo usando el diccionario
        if 'equipo_id' in df.columns:
            df['equipo_nombre'] = df['equipo_id'].map(equipos_dict)
        
        # Seleccionar columnas para mostrar
        cols_ordenadas = ['fecha_programada', 'equipo_nombre', 'tipo', 'prioridad', 'estado', 'descripcion']
        
        # Colorear según prioridad
        def color_prioridad(val):
            color = 'white'
            if val == 'urgente': color = '#ffcccc' # Rojo claro
            elif val == 'alta': color = '#ffe6cc'    # Naranja claro
            elif val == 'baja': color = '#e6ffcc'    # Verde claro
            return f'background-color: {color}'

        st.dataframe(
            df[cols_ordenadas].style.applymap(color_prioridad, subset=['prioridad']),
            use_container_width=True,
            height=400
        )
    else:
        st.info("No hay mantenimientos registrados.")

# --- TAB 2: NUEVO MANTENIMIENTO ---
with tab2:
    st.subheader("Programar Nuevo Mantenimiento")
    
    if not equipos:
        st.warning("⚠️ No se encontraron equipos. Registra equipos primero en la sección 'Equipos'.")
    else:
        with st.form("form_mantenimiento"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Selectbox que muestra "Codigo - Nombre" pero retorna el ID
                equipo_id = st.selectbox(
                    "Seleccionar Equipo *",
                    options=list(equipos_dict.keys()),
                    format_func=lambda x: equipos_dict[x]
                )
                
                tipo = st.selectbox("Tipo de Mantenimiento", ["preventivo", "correctivo"])
                prioridad = st.selectbox("Prioridad", ["baja", "media", "alta", "urgente"])
                
            with col2:
                fecha_prog = st.date_input("Fecha Programada *", value=date.today())
                descripcion = st.text_area("Descripción / Problema detectado", height=100)
            
            submitted = st.form_submit_button("📅 Programar", use_container_width=True)
            
            if submitted:
                nuevo_mant = {
                    "equipo_id": equipo_id,
                    "tipo": tipo,
                    "fecha_programada": str(fecha_prog),
                    "descripcion": descripcion,
                    "prioridad": prioridad
                }
                
                try:
                    # Enviar petición al API Gateway (que redirige al microservicio)
                    # Nota: La URL debe coincidir con la ruta definida en el Gateway
                    response = requests.post(
                        f"{API_URL}/api/mantenimientos", # Asegúrate de que esta ruta esté en el Gateway
                        json=nuevo_mant,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Mantenimiento programado exitosamente")
                    else:
                        st.error(f"❌ Error al programar: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")