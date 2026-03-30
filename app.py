import streamlit as st
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Innovación Abierta Perú",
    page_icon="🇵🇪",
    layout="wide"
)

# --- 2. CONEXIÓN ROBUSTA A FIREBASE ---
@st.cache_resource
def iniciar_db():
    # Evita inicializar múltiples veces la misma App
    if not firebase_admin._apps:
        try:
            # Obtener credenciales desde los Secrets de Streamlit
            creds_dict = dict(st.secrets["firebase"])
            # Limpieza de la clave privada (manejo de saltos de línea)
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error de configuración en Firebase: {e}")
            return None
    
    # IMPORTANTE: Forzamos la conexión a la base de datos '(default)'
    return firestore.client()

# Inicializamos el cliente de base de datos
db = iniciar_db()

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
        padding: 0.5rem; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #d4af37; color: black; border: 1px solid #fff; }
    
    /* Estilo para las tarjetas de retos */
    .reto-card {
        padding: 20px; border: 1px solid #333; border-radius: 15px; 
        background: #111; margin-bottom: 15px;
    }
    
    /* Ajuste de inputs para que se vean oscuros */
    input, select, textarea {
        background-color: #1a1a1a !important; color: white !important; border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h2 style='color: #d4af37;'>Panel de Control</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("Ir a:", ["🏠 Inicio", "👥 Registro Talento", "🏢 Publicar Reto", "🎯 Muro de Retos", "💬 Chat Comunitario"])

# --- 5. LÓGICA DE LAS SECCIONES ---

# SECCIÓN: INICIO
if menu == "🏠 Inicio":
    st.markdown('<h1 class="main-title">Plataforma de Innovación Abierta</h1>', unsafe_allow_html=True)
    st.subheader("Conectando la Ciencia Renacyt con los Retos de la Industria")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🧬 **Oferta de Innovación:** Investigadores Renacyt y Emprendedores Dinámicos listos para proponer soluciones.")
    with col2:
        st.success("🏢 **Demanda de Innovación:** Empresas e Instituciones que publican sus brechas tecnológicas y retos.")
    
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200", caption="Ecosistema de Innovación Peruana")

# SECCIÓN: REGISTRO TALENTO
elif menu == "👥 Registro Talento":
    st.header("Registro de Investigadores y Emprendedores")
    with st.form("form_talento"):
        nombre = st.text_input("Nombre Completo o Startup")
        perfil = st.selectbox("Categoría de Actor", ["Investigador Renacyt", "Emprendedor Dinámico"])
        region = st.selectbox("Región de Origen", ["Lima", "Arequipa", "Cusco", "Piura", "La Libertad", "Junín", "Puno", "Otros"])
        especialidad = st.text_area("Describa su especialidad o solución tecnológica")
        clave = st.text_input("Defina una clave básica", type="password")
        
        if st.form_submit_button("Registrar Perfil"):
            if db and nombre and clave:
                try:
                    # Guardar en la colección 'usuarios' de Firestore
                    db.collection("usuarios").add({
                        "nombre": nombre, "perfil": perfil, "region": region,
                        "especialidad": especialidad, "clave": clave, "fecha": datetime.now()
                    })
                    st.success(f"¡Excelente {nombre}! Tu perfil ha sido registrado en la base de datos.")
                except Exception as e:
                    st.error(f"Error al conectar con la base de datos: {e}")
            else:
                st.warning("Por favor, completa los campos de Nombre y Clave.")

# SECCIÓN: PUBLICAR RETO
elif menu == "🏢 Publicar Reto":
    st.header("Portal para Empresas e Instituciones")
    st.write("Publique aquí sus retos de innovación para recibir propuestas del talento nacional.")
    
    with st.form("form_reto"):
        empresa = st.text_input("Nombre de la Institución/Empresa")
        titulo_reto = st.text_input("Título del Reto (Necesidad)")
        descripcion = st.text_area("Descripción detallada del desafío técnico")
        reg_impacto = st.selectbox("Región del Reto", ["Nacional", "Lima", "Arequipa", "Piura", "Cusco"])
        
        if st.form_submit_button("Publicar Desafío"):
            if db and empresa and titulo_reto:
                try:
                    db.collection("retos").add({
                        "empresa": empresa, "reto": titulo_reto, "descripcion": descripcion,
                        "region": reg_impacto, "fecha": datetime.now()
                    })
                    st.balloons()
                    st.success("El reto ha sido publicado exitosamente en el muro.")
                except Exception as e:
                    st.error(f"Error al publicar el reto: {e}")
            else:
                st.warning("Debes completar el nombre de la empresa y el título del reto.")

# SECCIÓN: MURO DE RETOS
elif menu == "🎯 Muro de Retos":
    st.header("🎯 Matchmaking: Retos de Innovación")
    
    if db:
        try:
            # Consultar retos ordenados por fecha
            retos_ref = db.collection("retos").order_by("fecha", direction=firestore.Query.DESCENDING).stream()
            
            hay_retos = False
            for r in retos_ref:
                hay_retos = True
                data = r.to_dict()
                st.markdown(f"""
                <div class="reto-card">
                    <h3 style="color: #d4af37; margin-bottom: 5px;">{data['reto']}</h3>
                    <p style="color: #888; font-size: 0.9rem;">🏢 {data['empresa']} | 📍 {data['region']}</p>
                    <p style="color: #ddd;">{data['descripcion']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Postular a {data['empresa']}", key=r.id):
                    st.info(f"Conectando con {data['empresa']}... (Función disponible en v2.1)")
            
            if not hay_retos:
                st.info("Aún no hay retos publicados. ¡Invita a las empresas a participar!")
        except Exception as e:
            st.error(f"Error al cargar el muro: {e}")

# SECCIÓN: CHAT
elif menu == "💬 Chat Comunitario":
    st.header("💬 Espacio de Networking")
    st.markdown("---")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial de mensajes
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # Entrada de nuevo mensaje
    if prompt := st.chat_input("Escribe una propuesta o consulta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.caption("Plataforma Innovación Abierta v2.0")
st.sidebar.caption("Conectado a Google Firebase 🔥")
