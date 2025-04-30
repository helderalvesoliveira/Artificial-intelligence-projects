import streamlit as st
from tabs.resume_transcriptions import show_resume_transcriptions
from tabs.documents_search import show_documents_search   
from dotenv import load_dotenv
load_dotenv(override=True)

st.set_page_config(page_title="MeetDocAI", layout="wide")
st.title("📑 MeetDocAI - Sistema de Resumo e Consulta de Documentos")

aba = st.sidebar.radio("Escolha uma ferramenta:", [
                       "📝 Resumo de Reuniões", "📂 Consulta Documentos (RAG)"])

# --- Estado Inicial ---
if "resumo_gerado" not in st.session_state:
    st.session_state.resumo_gerado = ""
    st.session_state.modo_edicao = False

# === RESUMO DE REUNIÕES ===
if aba == "📝 Resumo de Reuniões":
    show_resume_transcriptions()


# === CONSULTA DE DOCUMENTOS ===
elif aba == "📂 Consulta Documentos (RAG)":
   show_documents_search()