import streamlit as st
from agents.meeting_summary_agent import resume_transcription
from agents.send_email_agent import crew
from agents.my_custom_listener import MyCustomListener
import os

def show_resume_transcriptions():
    st.header("📝 Resumo Automático de Reuniões")
    st.markdown(
        "Faça upload de uma transcrição `.txt` para gerar um resumo estruturado da reunião.")

    uploaded_file = st.file_uploader(
        "Carregue a transcrição da reunião (.txt)", type=["txt"])

    if uploaded_file:
        transcript_text = uploaded_file.read().decode("utf-8")
        st.text_area("Transcrição da reunião", transcript_text, height=300)

        if st.button("Gerar Resumo", key="gerar_resumo_btn"):
            with st.spinner("⏳ A gerar o resumo com IA (CrewAI)..."):
                placeholder_info = st.empty()
                placeholder_info.info(
                    "🔍 A processar sua transcrição (preview)")
                resposta_placeholder = st.empty()

                listener = MyCustomListener(placeholder=resposta_placeholder)
                try:
                    resumo = resume_transcription(
                        transcript_text, listener=listener)
                finally:
                    resposta_placeholder.markdown(listener.current_text)
                placeholder_info.empty()
                resposta_placeholder.empty()
                st.session_state.resumo_gerado = resumo
                st.session_state.modo_edicao = False
                st.success("✅ Resumo gerado com sucesso!")

    # === Edição ou Visualização ===
    if st.session_state.get("resumo_gerado"):
        st.markdown("### 📝 Editar Resumo" if st.session_state.get(
            "modo_edicao") else "### ✅ Resumo Gerado:")

        if st.session_state.get("modo_edicao"):
            novo_texto = st.text_area(
                "Resumo Editável", st.session_state["resumo_gerado"], height=300)
        else:
            st.markdown(st.session_state["resumo_gerado"])

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.session_state.get("modo_edicao"):
                if st.button("✅ Concluir Edição", key="concluir_edicao"):
                    st.session_state["resumo_gerado"] = novo_texto
                    st.session_state["modo_edicao"] = False
                    with open("ata_reuniao.txt", "w", encoding="utf-8") as f:
                        f.write(st.session_state["resumo_gerado"])
                    st.rerun()
            else:
                if st.button("✏️ Editar Resumo", key="editar_resumo"):
                    st.session_state["modo_edicao"] = True
                    st.rerun()

        with col2:
                if st.button("📤 Enviar por Email", key="enviar_email"):
                    crew.kickoff()
                    st.rerun()

        with col3:
            if st.button("🗑️ Limpar Resumo", key="limpar_resumo"):
                st.session_state.resumo_gerado = ""
                st.session_state.modo_edicao = False
                st.success("🧼 Resumo limpo com sucesso!")
                st.rerun()