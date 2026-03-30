import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Innovación Abierta Perú", page_icon="🇵🇪", layout="wide")

# Conexión usando los Secrets configurados
conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .main-title {
        font-size: 3rem; font-weight: 800;
        background: -webkit-linear-gradient(#d4af37, #fcf6ba);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%; border-radius: 12px; border: 1px solid #d4af37;
        background-color: #1a1a1a; color: #d4af37; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Innovación Abierta Perú</h1>', unsafe_allow_html=True)

menu = st.sidebar.radio("Ir a:", ["🏠 Inicio", "👥 Registro Talento", "🎯 Muro de Retos"])

if menu == "👥 Registro Talento":
    st.header("Registro de Investigadores")
    with st.form("form_registro"):
        nombre = st.text_input("Nombre / Startup")
        perfil = st.selectbox("Perfil", ["Investigador Renacyt", "Emprendedor Dinámico"])
        region = st.selectbox("Región", ["Lima", "Arequipa", "Cusco", "Piura", "Otros"])
        especialidad = st.text_area("Especialidad")
        clave = st.text_input("Clave", type="password")
        
        if st.form_submit_button("Registrar Perfil"):
            if nombre and clave:
                try:
                    # LEER: Obtenemos los datos actuales
                    df_existente = conn.read()
                    
                    # CREAR: Nuevo registro
                    nuevo_registro = {
                        "nombre": nombre,
                        "perfil": perfil,
                        "region": region,
                        "especialidad": especialidad,
                        "clave": clave,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # ACTUALIZAR: Añadimos la fila y subimos
                    df_actualizado = pd.concat([df_existente, pd.DataFrame([nuevo_registro])], ignore_index=True)
                    conn.update(data=df_actualizado)
                    
                    st.balloons()
                    st.success("¡Registro exitoso! Los datos se han guardado en el Google Sheet.")
                except Exception as e:
                    st.error(f"Error técnico: {e}")
            else:
                st.warning("Completa los campos obligatorios.")

elif menu == "🎯 Muro de Retos":
    st.header("🎯 Talentos y Retos Registrados")
    try:
        df = conn.read()
        st.dataframe(df.drop(columns=["clave"], errors='ignore'), use_container_width=True)
    except:
        st.info("No hay datos disponibles aún.")
