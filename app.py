import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Innovación Abierta Perú",
    page_icon="🇵🇪",
    layout="wide"
)

# --- 2. CONEXIÓN A GOOGLE SHEETS ---
# Usamos el link que me proporcionaste
url_sheet = "https://docs.google.com/spreadsheets/d/1uxq3CklaSh1lsn9Sx4lFN1AN9lDnVIPJKhH8UOjaTbo/edit?gid=0#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. ESTILO VISUAL PREMIUM (DARK MODE) ---
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
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #d4af37; color: black; }
    div[data-testid="stExpander"] {
        background-color: #111111 !important;
        border: 1px solid #333333 !important;
    }
    input, select, textarea {
        background-color: #1a1a1a !important; color: white !important; border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVEGACIÓN ---
st.markdown('<h1 class="main-title">Innovación Abierta Perú</h1>', unsafe_allow_html=True)
menu = st.sidebar.radio("Ir a:", ["🏠 Inicio", "👥 Registro Talento", "🏢 Publicar Reto", "🎯 Muro de Retos"])

# --- 5. SECCIONES ---

if menu == "🏠 Inicio":
    st.subheader("Ecosistema Digital de Innovación")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🧬 **Oferta:** Investigadores Renacyt y Emprendedores Dinámicos.")
    with col2:
        st.success("🏢 **Demanda:** Empresas que buscan soluciones tecnológicas.")
    st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200")

elif menu == "👥 Registro Talento":
    st.header("Registro de Investigadores y Emprendedores")
    with st.form("form_registro"):
        nombre = st.text_input("Nombre / Institución")
        perfil = st.selectbox("Perfil", ["Investigador Renacyt", "Emprendedor Dinámico"])
        region = st.selectbox("Región", ["Lima", "Arequipa", "Cusco", "Piura", "La Libertad", "Puno", "Otros"])
        especialidad = st.text_area("Describa su especialidad o solución")
        clave = st.text_input("Clave básica", type="password")
        
        if st.form_submit_button("Registrar Perfil"):
            if nombre and clave:
                try:
                    # Leer datos actuales para no borrar lo anterior
                    df_actual = conn.read(spreadsheet=url_sheet)
                    
                    # Nuevo registro
                    nuevo_registro = pd.DataFrame([{
                        "nombre": nombre,
                        "perfil": perfil,
                        "region": region,
                        "especialidad": especialidad,
                        "clave": clave,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    
                    # Unir y actualizar
                    df_final = pd.concat([df_actual, nuevo_registro], ignore_index=True)
                    conn.update(spreadsheet=url_sheet, data=df_final)
                    
                    st.balloons()
                    st.success(f"¡Excelente {nombre}! Ya eres parte de la red nacional.")
                except Exception as e:
                    st.error(f"Error al conectar con Google Sheets: {e}")
            else:
                st.warning("Completa el nombre y la clave por favor.")

elif menu == "🎯 Muro de Retos":
    st.header("🎯 Retos de Innovación Publicados")
    try:
        # Mostramos los datos registrados para ver el "Match"
        df_registrados = conn.read(spreadsheet=url_sheet)
        if not df_registrados.empty:
            st.write("Explora el talento y retos actuales en el sistema:")
            # Ocultamos la clave por seguridad al mostrar la tabla
            st.dataframe(df_registrados.drop(columns=["clave"], errors='ignore'), use_container_width=True)
        else:
            st.info("Aún no hay registros en la base de datos.")
    except:
        st.info("La base de datos está iniciando. Registra el primer talento.")

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.caption("v2.5 - Base de Datos en Google Sheets Active")
