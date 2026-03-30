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
# La conexión usará los Secrets (Service Account) para tener permisos de ESCRITURA
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

# --- 4. NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h2 style='color: #d4af37;'>Menú Principal</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("Seleccione una opción:", 
    ["🏠 Inicio", "👥 Registro Talento (Investigadores)", "🏢 Publicar Reto (Empresas)", "🎯 Muro de Matchmaking"])

# --- 5. LÓGICA DE LAS SECCIONES ---

# --- SECCIÓN: INICIO ---
if menu == "🏠 Inicio":
    st.markdown('<h1 class="main-title">Innovación Abierta Perú</h1>', unsafe_allow_html=True)
    st.subheader("Conectando el Conocimiento con la Industria")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🧬 **Para Investigadores:** Registra tu perfil Renacyt y encuentra retos que resolver.")
    with col2:
        st.success("🏢 **Para Empresas:** Publica tus brechas tecnológicas y encuentra al experto ideal.")
    
    st.image("https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?auto=format&fit=crop&w=1200", caption="Impulsando la Ciencia y Tecnología en el Perú")

# --- SECCIÓN: REGISTRO TALENTO ---
elif menu == "👥 Registro Talento (Investigadores)":
    st.header("Registro de Oferta Tecnológica")
    with st.form("form_talento"):
        nombre = st.text_input("Nombre Completo / Startup")
        perfil = st.selectbox("Perfil", ["Investigador Renacyt", "Emprendedor Dinámico", "Consultor Tecnológico"])
        region = st.selectbox("Región", ["Lima", "Arequipa", "Cusco", "Piura", "La Libertad", "Junín", "Otros"])
        especialidad = st.text_area("Describa su especialidad o solución técnica")
        clave = st.text_input("Defina una clave", type="password")
        
        if st.form_submit_button("Guardar Mi Perfil"):
            if nombre and clave:
                try:
                    # Leer datos actuales (Pestaña 'Talento' o por defecto)
                    df_existente = conn.read()
                    
                    nuevo_id = f"T-{datetime.now().strftime('%M%S')}"
                    nuevo_registro = pd.DataFrame([{
                        "ID": nuevo_id,
                        "Tipo": "TALENTO",
                        "Entidad": nombre,
                        "Categoria": perfil,
                        "Region": region,
                        "Detalle": especialidad,
                        "Clave": clave,
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    
                    df_final = pd.concat([df_existente, nuevo_registro], ignore_index=True)
                    conn.update(data=df_final)
                    
                    st.balloons()
                    st.success(f"¡Bienvenido {nombre}! Tu perfil se guardó correctamente.")
                except Exception as e:
                    st.error(f"Error técnico al guardar: {e}")
            else:
                st.warning("El nombre y la clave son obligatorios.")

# --- SECCIÓN: PUBLICAR RETO (EMPRESAS) ---
elif menu == "🏢 Publicar Reto (Empresas)":
    st.header("Portal de Demandas Tecnológicas")
    with st.form("form_empresa"):
        empresa = st.text_input("Nombre de la Empresa / Institución")
        titulo_reto = st.text_input("Título del Reto (¿Qué necesita solucionar?)")
        descripcion = st.text_area("Detalles del desafío o problema técnico")
        prioridad = st.select_slider("Prioridad del Reto", options=["Baja", "Media", "Alta"])
        region_reto = st.selectbox("Región del Reto", ["Nacional", "Lima", "Arequipa", "Piura", "Cusco"])
        
        if st.form_submit_button("Publicar Desafío en el Muro"):
            if empresa and titulo_reto:
                try:
                    df_existente = conn.read()
                    
                    nuevo_id = f"R-{datetime.now().strftime('%M%S')}"
                    nuevo_reto = pd.DataFrame([{
                        "ID": nuevo_id,
                        "Tipo": "RETO",
                        "Entidad": empresa,
                        "Categoria": titulo_reto,
                        "Region": region_reto,
                        "Detalle": descripcion,
                        "Clave": "RETO-PUBLICO",
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    
                    df_final = pd.concat([df_existente, nuevo_reto], ignore_index=True)
                    conn.update(data=df_final)
                    
                    st.success("¡Reto publicado! Los investigadores ya pueden verlo en el muro.")
                except Exception as e:
                    st.error(f"Error al conectar con la base de datos: {e}")
            else:
                st.warning("Completa el nombre de la empresa y el título del reto.")

# --- SECCIÓN: MURO DE MATCHMAKING ---
elif menu == "🎯 Muro de Matchmaking":
    st.header("🎯 Muro de Innovación")
    st.write("Explora los retos publicados y el talento disponible.")
    
    try:
        df = conn.read()
        if not df.empty:
            tab1, tab2 = st.tabs(["🚀 Retos de Empresas", "👤 Talentos Registrados"])
            
            with tab1:
                retos = df[df["Tipo"] == "RETO"]
                if not retos.empty:
                    for _, row in retos.iterrows():
                        st.markdown(f"""
                        <div class="card">
                            <h3 style="color: #d4af37;">🔥 {row['Categoria']}</h3>
                            <p><b>Empresa:</b> {row['Entidad']} | <b>Región:</b> {row['Region']}</p>
                            <p>{row['Detalle']}</p>
                            <small>Publicado: {row['Fecha']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No hay retos publicados aún.")
            
            with tab2:
                talento = df[df["Tipo"] == "TALENTO"]
                if not talento.empty:
                    for _, row in talento.iterrows():
                        st.markdown(f"""
                        <div class="card" style="border-left: 5px solid #d4af37;">
                            <h4 style="color: #fff;">👤 {row['Entidad']}</h4>
                            <p><b>Perfil:</b> {row['Categoria']} | <b>Región:</b> {row['Region']}</p>
                            <p><i>Especialidad:</i> {row['Detalle']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("La base de datos está vacía. Sé el primero en registrarte.")
    except Exception as e:
        st.error(f"Error al cargar el muro: {e}")

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.caption("v3.0 - Innovación Abierta Perú")
st.sidebar.caption("Powered by Google Sheets & Streamlit")
