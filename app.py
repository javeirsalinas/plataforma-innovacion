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
# Se conecta usando los Secrets (Service Account) para permisos de escritura
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
        padding: 0.6rem; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #d4af37; color: black; border: 1px solid #fff; }
    
    .card {
        padding: 20px; border: 1px solid #333; border-radius: 15px; 
        background: #111; margin-bottom: 15px;
    }
    input, select, textarea {
        background-color: #1a1a1a !important; color: white !important; border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNCIÓN AUXILIAR DE GUARDADO ---
def guardar_en_gsheets(nueva_fila_dict):
    try:
        # Intentamos leer la hoja actual
        try:
            df_existente = conn.read()
            # Si la hoja existe pero está vacía de datos (solo encabezados o nada)
            if df_existente is None or df_existente.empty:
                 df_existente = pd.DataFrame(columns=["ID", "Tipo", "Entidad", "Categoria", "Region", "Detalle", "Clave", "Fecha"])
        except:
            # Si falla la lectura, creamos la estructura desde cero
            df_existente = pd.DataFrame(columns=["ID", "Tipo", "Entidad", "Categoria", "Region", "Detalle", "Clave", "Fecha"])

        # Crear el nuevo registro como DataFrame
        df_nuevo = pd.DataFrame([nueva_fila_dict])
        
        # Concatenar asegurando que no haya filas totalmente vacías
        df_existente = df_existente.dropna(how='all')
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        
        # Actualizar la hoja de Google
        conn.update(data=df_final)
        return True
    except Exception as e:
        st.error(f"Error técnico de conexión: {e}")
        return False

# --- 5. NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h2 style='color: #d4af37;'>Panel Innovación</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("Ir a:", 
    ["🏠 Inicio", "👥 Registro Talento", "🏢 Publicar Reto", "🎯 Muro de Matchmaking"])

# --- 6. LÓGICA DE LAS SECCIONES ---

if menu == "🏠 Inicio":
    st.markdown('<h1 class="main-title">Innovación Abierta Perú</h1>', unsafe_allow_html=True)
    st.subheader("La plataforma que une la Ciencia con la Empresa")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🧬 **Investigadores:** Registren su oferta tecnológica.")
    with col2:
        st.success("🏢 **Empresas:** Publiquen sus desafíos técnicos.")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")

elif menu == "👥 Registro Talento":
    st.header("Registro de Oferta Tecnológica")
    with st.form("form_talento"):
        nombre = st.text_input("Nombre Completo / Startup")
        perfil = st.selectbox("Perfil", ["Investigador Renacyt", "Emprendedor Dinámico", "Consultor"])
        region = st.selectbox("Región", ["Lima", "Arequipa", "Cusco", "Piura", "La Libertad", "Otros"])
        especialidad = st.text_area("Describa su especialidad")
        clave = st.text_input("Contraseña", type="password")
        
        if st.form_submit_button("Registrar Perfil"):
            if nombre and clave:
                exito = guardar_en_gsheets({
                    "ID": f"T-{datetime.now().strftime('%H%M%S')}",
                    "Tipo": "TALENTO",
                    "Entidad": nombre,
                    "Categoria": perfil,
                    "Region": region,
                    "Detalle": especialidad,
                    "Clave": clave,
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                if exito:
                    st.balloons()
                    st.success(f"¡Bienvenido {nombre}! Perfil guardado en el Excel.")
            else:
                st.warning("Nombre y clave son campos obligatorios.")

elif menu == "🏢 Publicar Reto":
    st.header("Portal de Demandas (Empresas)")
    with st.form("form_reto"):
        empresa = st.text_input("Empresa / Institución")
        titulo = st.text_input("Título del Reto")
        desc = st.text_area("¿Cuál es el desafío técnico?")
        reg_reto = st.selectbox("Ubicación del Reto", ["Nacional", "Lima", "Arequipa", "Piura", "Cusco"])
        
        if st.form_submit_button("Publicar Reto"):
            if empresa and titulo:
                exito = guardar_en_gsheets({
                    "ID": f"R-{datetime.now().strftime('%H%M%S')}",
                    "Tipo": "RETO",
                    "Entidad": empresa,
                    "Categoria": titulo,
                    "Region": reg_reto,
                    "Detalle": desc,
                    "Clave": "RETO-PUBLICO",
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                if exito:
                    st.success("Reto publicado con éxito en la plataforma.")
            else:
                st.warning("Empresa y Título son campos obligatorios.")

elif menu == "🎯 Muro de Matchmaking":
    st.header("🎯 Muro de Innovación")
    try:
        df = conn.read()
        if df is not None and not df.empty:
            tab1, tab2 = st.tabs(["🚀 Retos de Empresas", "👤 Talentos Registrados"])
            
            with tab1:
                retos = df[df["Tipo"] == "RETO"]
                for _, row in retos.iterrows():
                    st.markdown(f'<div class="card"><h3 style="color:#d4af37;">🔥 {row["Categoria"]}</h3><p><b>Empresa:</b> {row["Entidad"]} | 📍 {row["Region"]}</p><p>{row["Detalle"]}</p></div>', unsafe_allow_html=True)
            
            with tab2:
                talento = df[df["Tipo"] == "TALENTO"]
                for _, row in talento.iterrows():
                    st.markdown(f'<div class="card" style="border-left:5px solid #d4af37;"><h4 style="color:#fff;">👤 {row["Entidad"]}</h4><p><b>Perfil:</b> {row["Categoria"]} | 📍 {row["Region"]}</p><p><i>Especialidad:</i> {row["Detalle"]}</p></div>', unsafe_allow_html=True)
        else:
            st.info("Aún no hay datos. ¡Sé el primero en registrarte!")
    except:
        st.info("La base de datos está inicializándose.")

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.caption("v4.0 - Innovación Abierta Perú")
