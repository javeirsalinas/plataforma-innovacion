import streamlit as st
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Innovación Abierta Perú", page_icon="🇵🇪", layout="wide")

# --- CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    # Lee las credenciales desde los Secrets de Streamlit
    firebase_creds = dict(st.secrets["firebase"])
    # Corregir el formato de la private_key que a veces se corta al pegar
    firebase_creds["private_key"] = firebase_creds["private_key"].replace("\\n", "\n")
    
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- ESTILO CSS PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .main-title {
        font-size: 2.5rem; font-weight: 800;
        background: -webkit-linear-gradient(#d4af37, #fcf6ba);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .stButton>button {
        border-radius: 10px; border: 1px solid #d4af37;
        background-color: #1a1a1a; color: #d4af37;
    }
    .stButton>button:hover { background-color: #d4af37; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Innovación Abierta Perú 🇵🇪</h1>', unsafe_allow_html=True)

menu = st.sidebar.radio("Menú Principal", ["🏠 Inicio", "👥 Registro Talento", "🏢 Publicar Reto", "🎯 Muro de Retos", "💬 Chat"])

# --- FUNCIONES DE BASE DE DATOS ---
def guardar_usuario(datos):
    db.collection("usuarios").add(datos)

def guardar_reto(datos):
    db.collection("retos").add(datos)

def obtener_retos():
    retos_ref = db.collection("retos").order_by("fecha", direction=firestore.Query.DESCENDING)
    return [doc.to_dict() for doc in retos_ref.stream()]

# --- SECCIÓN: INICIO ---
if menu == "🏠 Inicio":
    st.markdown("### Bienvenido al Ecosistema de Innovación")
    st.write("Conectamos la demanda tecnológica de las empresas con la oferta científica de los investigadores Renacyt.")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1000", caption="Tecnología y Futuro para el Perú")

# --- SECCIÓN: REGISTRO TALENTO ---
elif menu == "👥 Registro Talento":
    st.header("Registro de Investigadores y Emprendedores")
    with st.form("registro_talento"):
        nombre = st.text_input("Nombre / Startup")
        perfil = st.selectbox("Perfil", ["Investigador Renacyt", "Emprendedor Dinámico"])
        region = st.selectbox("Región", ["Lima", "Arequipa", "Cusco", "Piura", "La Libertad", "Junín", "Puno", "Otros"])
        especialidad = st.text_area("Especialidad técnica o solución")
        clave = st.text_input("Clave básica", type="password")
        
        if st.form_submit_button("Registrar Perfil"):
            if nombre and clave:
                guardar_usuario({
                    "nombre": nombre, "perfil": perfil, 
                    "region": region, "especialidad": especialidad,
                    "clave": clave, "fecha_reg": datetime.now()
                })
                st.success(f"¡Perfil de {nombre} guardado en la base de datos!")
            else:
                st.error("Por favor completa los campos obligatorios.")

# --- SECCIÓN: PUBLICAR RETO ---
elif menu == "🏢 Publicar Reto":
    st.header("Portal para Empresas e Instituciones")
    with st.form("form_reto"):
        empresa = st.text_input("Nombre de la Institución")
        titulo_reto = st.text_input("Título del Reto de Innovación")
        descripcion = st.text_area("Descripción del desafío")
        region_reto = st.selectbox("Región de impacto", ["Lima", "Arequipa", "Piura", "Cusco", "Nacional"])
        
        if st.form_submit_button("Publicar Desafío"):
            guardar_reto({
                "empresa": empresa, "reto": titulo_reto, 
                "descripcion": descripcion, "region": region_reto,
                "fecha": datetime.now()
            })
            st.balloons()
            st.success("Reto publicado globalmente.")

# --- SECCIÓN: MURO DE RETOS ---
elif menu == "🎯 Muro de Retos":
    st.header("🎯 Desafíos Disponibles")
    retos = obtener_retos()
    
    if not retos:
        st.info("Aún no hay retos publicados. ¡Sé el primero!")
    else:
        for r in retos:
            with st.container():
                st.markdown(f"""
                <div style="padding:15px; border-radius:10px; border:1px solid #333; margin-bottom:10px; background:#111;">
                    <h3 style="color:#d4af37; margin:0;">{r['reto']}</h3>
                    <p style="font-size:0.9rem; color:#888;">{r['empresa']} | 📍 {r['region']}</p>
                    <p>{r['descripcion']}</p>
                </div>
                """, unsafe_allow_html=True)

# --- SECCIÓN: CHAT ---
elif menu == "💬 Chat":
    st.header("Chat de Networking")
    st.write("Próximamente: Historial de chat persistente en Firebase.")
    if prompt := st.chat_input("Escribe un mensaje a la comunidad..."):
        with st.chat_message("user"):
            st.write(prompt)
