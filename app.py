import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Innovación Abierta Perú",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS PREMIUM (DARK MODE) ---
st.markdown("""
    <style>
    /* Fondo principal y textos */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Títulos con degradado */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#d4af37, #fcf6ba);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Botones personalizados */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #d4af37;
        background-color: #1a1a1a;
        color: #d4af37;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #d4af37;
        color: #000000;
    }

    /* Tarjetas visuales (Cards) */
    .css-1r6slb0, .stExpander {
        background-color: #111111 !important;
        border: 1px solid #333333 !important;
        border-radius: 15px !important;
    }
    
    /* Inputs y Selectores */
    input, select, textarea {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS TEMPORALES (Simulación hasta conectar Firebase) ---
if "bd_usuarios" not in st.session_state:
    st.session_state.bd_usuarios = []
if "bd_retos" not in st.session_state:
    st.session_state.bd_retos = [
        {"empresa": "Minera del Sur", "reto": "Optimización de relaves hídricos", "region": "Arequipa", "fecha": "2024-05-20"},
        {"empresa": "AgroChira SAC", "reto": "Detección temprana de plagas en banano", "region": "Piura", "fecha": "2024-05-21"}
    ]
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- INTERFAZ DE USUARIO ---

st.markdown('<h1 class="main-title">Innovación Abierta Perú</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>El puente entre la ciencia de Renacyt, el empuje emprendedor y los retos de la industria peruana.</p>", unsafe_allow_html=True)

# Barra lateral para navegación
st.sidebar.image("https://www.gob.pe/images/guides/1594119615.jpg", width=100) # Opcional: logo Concytec o similar
menu = st.sidebar.radio("Navegación", ["🏠 Inicio", "👥 Registro de Talento", "🏢 Portal de Empresas", "🎯 Muro de Retos", "💬 Chat Comunitario"])

# --- SECCIÓN: INICIO ---
if menu == "🏠 Inicio":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧬 Para Investigadores y Emprendedores")
        st.write("Registra tu perfil Renacyt o tu Startup dinámica para acceder a desafíos reales pagados por empresas e instituciones del estado.")
    with col2:
        st.markdown("### 🏢 Para Empresas e Instituciones")
        st.write("Publica tus brechas tecnológicas y necesidades de innovación para recibir propuestas de la comunidad científica de todo el Perú.")
    
    st.divider()
    st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200", caption="Innovación Tecnológica Peruana")

# --- SECCIÓN: REGISTRO TALENTO ---
elif menu == "👥 Registro de Talento":
    st.header("Registro de Oferta Tecnológica")
    with st.form("form_talento"):
        nombre = st.text_input("Nombre Completo o Razón Social")
        perfil = st.selectbox("Perfil del Actor", ["Investigador Renacyt", "Emprendedor Dinámico"])
        region = st.selectbox("Región de Origen", ["Amazonas", "Ancash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali"])
        especialidad = st.text_area("Describa su solución o área de investigación")
        clave = st.text_input("Clave de acceso (Básica)", type="password")
        
        if st.form_submit_button("Crear Perfil"):
            nuevo_user = {"nombre": nombre, "tipo": perfil, "region": region, "clave": clave}
            st.session_state.bd_usuarios.append(nuevo_user)
            st.success(f"¡Bienvenido {nombre}! Tu perfil ha sido registrado exitosamente en {region}.")

# --- SECCIÓN: PORTAL EMPRESAS ---
elif menu == "🏢 Portal de Empresas":
    st.header("Publicar Demanda de Innovación")
    with st.expander("📝 Registrar Nueva Empresa"):
        emp_nombre = st.text_input("Nombre de la Empresa / Institución")
        emp_rubro = st.text_input("Sector (Minería, Salud, Agro, etc.)")
        emp_region = st.selectbox("Sede del Reto", ["Lima", "Arequipa", "Piura", "Cusco", "Otros"])
    
    with st.form("form_reto"):
        st.markdown("### Publicar un Reto")
        titulo_reto = st.text_input("Título del Reto (Necesidad)")
        desc_reto = st.text_area("Descripción detallada del problema")
        if st.form_submit_button("Publicar Reto en el Muro"):
            st.session_state.bd_retos.append({
                "empresa": emp_nombre, 
                "reto": titulo_reto, 
                "region": emp_region,
                "fecha": datetime.now().strftime("%Y-%m-%d")
            })
            st.balloons()
            st.success("Reto publicado correctamente.")

# --- SECCIÓN: MURO DE RETOS ---
elif menu == "🎯 Muro de Retos":
    st.header("🎯 Match de Oportunidades")
    st.write("Filtrado por Región:")
    filtro_reg = st.selectbox("Seleccionar Región para ver retos", ["Todas"] + list(set([r['region'] for r in st.session_state.bd_retos])))
    
    for r in st.session_state.bd_retos:
        if filtro_reg == "Todas" or r['region'] == filtro_reg:
            with st.container():
                st.markdown(f"""
                <div style="padding: 20px; border: 1px solid #333; border-radius: 15px; margin-bottom: 10px;">
                    <h3 style="color: #d4af37;">{r['reto']}</h3>
                    <p>🏢 <b>Empresa:</b> {r['empresa']} | 📍 <b>Región:</b> {r['region']} | 📅 <b>Fecha:</b> {r['fecha']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Postular al Reto de {r['empresa']}", key=r['reto']):
                    st.info("Función de postulación habilitada en v2.0")

# --- SECCIÓN: CHAT ---
elif menu == "💬 Chat Comunitario":
    st.header("💬 Espacio de Networking")
    st.write("Interactúa con todos los actores de la plataforma.")
    
    # Mostrar mensajes
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            
    if prompt := st.chat_input("Escribe tu consulta o propuesta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.write("v1.0 Deployment - Prototipo Funcional")
