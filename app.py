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
    # Si la app ya está iniciada, no lo hace de nuevo
    if not firebase_admin._apps:
        try:
            # Diccionario desde los Secrets de Streamlit
            creds_dict = dict(st.secrets["firebase"])
            # Limpieza técnica de la clave privada
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error de configuración en Firebase: {e}")
            return None
    return firestore.client()

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
        width: 100%; border-radius: 10px; border: 1px solid #d4af37;
        background-color: #1a1a1a; color: #d4af37; font-weight: bold;
    }
    .stButton>button:hover { background-color: #d4af37; color: black; }
    div[data-testid="stExpander"], .css-1r6slb0 {
        background-color: #111111 !important;
        border: 1px solid #333333 !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFAZ Y NAVEGACIÓN ---
st.markdown('<h1 class="main-title">Innovación Abierta Perú</h1>', unsafe_allow_html=True)

menu = st.sidebar.radio("Menú", ["🏠 Inicio", "👥 Registro Talento", "🏢 Publicar Reto", "🎯 Muro de Retos", "💬 Chat"])

# --- 5. LÓGICA DE LAS SECCIONES ---

if menu == "🏠 Inicio":
    st.subheader("Conectando Ciencia e Industria")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🧬 **Investigadores:** Resuelvan retos reales y moneticen su conocimiento.")
    with col2:
        st.success("🏢 **Empresas:** Encuentren soluciones disruptivas en todo el Perú.")
    st.image("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1000", caption="El futuro de la innovación peruana")

elif menu == "👥 Registro Talento":
    st.header("Registro de Oferta Tecnológica")
    with st.form("form_talento"):
        nombre = st.text_input("Nombre / Startup")
        perfil = st.selectbox("Perfil", ["Investigador Renacyt", "Emprendedor Dinámico"])
        region = st.selectbox("Región", ["Amazonas", "Ancash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali"])
        especialidad = st.text_area("Especialidad técnica")
        clave = st.text_input("Clave de acceso", type="password")
        
        if st.form_submit_button("Registrar mi Perfil"):
            if db and nombre and clave:
                try:
                    db.collection("usuarios").add({
                        "nombre": nombre, "perfil": perfil, "region": region,
                        "especialidad": especialidad, "clave": clave, "fecha": datetime.now()
                    })
                    st.success(f"¡Bienvenido {nombre}! Tu perfil se guardó en la nube.")
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            else:
                st.warning("Completa todos los campos.")

elif menu == "🏢 Publicar Reto":
    st.header("Portal Corporativo")
    with st.form("form_reto"):
        empresa = st.text_input("Nombre de la Empresa")
        titulo = st.text_input("Título del Reto")
        desc = st.text_area("Descripción de la necesidad")
        reg_reto = st.selectbox("Región", ["Lima", "Arequipa", "Cusco", "Piura", "Otras"])
        
        if st.form_submit_button("Publicar Desafío"):
            if db and empresa and titulo:
                try:
                    db.collection("retos").add({
                        "empresa": empresa, "reto": titulo, "descripcion": desc,
                        "region": reg_reto, "fecha": datetime.now()
                    })
                    st.balloons()
                    st.success("Reto publicado exitosamente.")
                except Exception as e:
                    st.error(f"Error al publicar: {e}")

elif menu == "🎯 Muro de Retos":
    st.header("🎯 Matchmaking de Innovación")
    if db:
        retos_ref = db.collection("retos").order_by("fecha", direction=firestore.Query.DESCENDING).stream()
        for r in retos_ref:
            data = r.to_dict()
            with st.container():
                st.markdown(f"""
                <div style="padding:20px; border:1px solid #333; border-radius:15px; margin-bottom:15px; background:#111;">
                    <h3 style="color:#d4af37; margin-bottom:5px;">{data['reto']}</h3>
                    <p style="color:#888; font-size:0.8rem;">🏢 {data['empresa']} | 📍 {data['region']}</p>
                    <p>{data['descripcion']}</p>
                </div>
                """, unsafe_allow_html=True)

elif menu == "💬 Chat":
    st.header("💬 Espacio de Networking")
    st.info("Este chat permite comunicación abierta entre todos los actores.")
    if "msg_list" not in st.session_state:
        st.session_state.msg_list = []

    for m in st.session_state.msg_list:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    if prompt := st.chat_input("Escribe tu propuesta..."):
        st.session_state.msg_list.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.caption("Plataforma v2.0 - Firebase Active Connection")
