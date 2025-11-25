import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Gestión de Proveedores", page_icon="🏢", layout="wide")

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

st.title("🏢 Gestión de Proveedores")
st.markdown("---")

def get_proveedores():
    try:
        response = requests.get(f"{API_URL}/api/proveedores", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return []

# Tabs principales
tab1, tab2 = st.tabs(["📋 Lista de Proveedores", "➕ Nuevo Proveedor"])

# --- TAB 1: LISTADO ---
with tab1:
    st.subheader("Directorio de Proveedores")
    
    if st.button("🔄 Actualizar Lista"):
        st.rerun()

    proveedores = get_proveedores()

    if proveedores:
        df = pd.DataFrame(proveedores)
        
        # Seleccionar y renombrar columnas para la tabla
        columnas_mostrar = ['razon_social', 'ruc', 'telefono', 'email', 'contacto_nombre', 'sitio_web']
        # Filtramos solo las que existan en el DF por seguridad
        cols_validas = [c for c in columnas_mostrar if c in df.columns]
        
        df_display = df[cols_validas].copy()
        df_display.columns = [c.replace('_', ' ').title() for c in cols_validas]
        
        st.dataframe(df_display, use_container_width=True)
        
        st.markdown(f"**Total de proveedores:** {len(proveedores)}")
    else:
        st.info("No hay proveedores registrados o no se pudo conectar con el servicio.")

# --- TAB 2: REGISTRO ---
with tab2:
    st.subheader("Registrar Nuevo Proveedor")
    
    with st.form("form_nuevo_proveedor"):
        col1, col2 = st.columns(2)
        
        with col1:
            razon_social = st.text_input("Razón Social *")
            ruc = st.text_input("RUC *")
            telefono = st.text_input("Teléfono")
            email = st.text_input("Email")
            
        with col2:
            contacto_nombre = st.text_input("Nombre de Contacto")
            contacto_telefono = st.text_input("Teléfono de Contacto")
            sitio_web = st.text_input("Sitio Web")
            direccion = st.text_area("Dirección Física")
            
        notas = st.text_area("Notas Adicionales")
        
        submitted = st.form_submit_button("💾 Guardar Proveedor", use_container_width=True)
        
        if submitted:
            if not razon_social or not ruc:
                st.error("⚠️ La Razón Social y el RUC son obligatorios")
            else:
                nuevo_proveedor = {
                    "razon_social": razon_social,
                    "ruc": ruc,
                    "direccion": direccion,
                    "telefono": telefono,
                    "email": email,
                    "contacto_nombre": contacto_nombre,
                    "contacto_telefono": contacto_telefono,
                    "sitio_web": sitio_web,
                    "notas": notas
                }
                
                try:
                    response = requests.post(
                        f"{API_URL}/api/proveedores", 
                        json=nuevo_proveedor,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Proveedor registrado exitosamente")
                        # Opcional: st.balloons()
                    else:
                        st.error(f"❌ Error al registrar: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")