import streamlit as st
import os
from chromadb import PersistentClient
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.vectorstores import Chroma as LegacyChroma
from langchain_ollama.llms import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.globals import set_debug
import time

# set_debug(True)

# Configuração inicial
CHROMA_DIR = "./db"


def show_documents_search():
    model_name = "BAAI/bge-m3"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    # Setup ChromaDB
    client = PersistentClient(path=CHROMA_DIR)

    # Funções auxiliares
    def load_document(file):
        ext = os.path.splitext(file.name)[1]
        path = os.path.join("temp_uploads", file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        if ext == ".pdf":
            return PyPDFLoader(path).load()
        elif ext == ".docx":
            return UnstructuredWordDocumentLoader(path).load()
        return None

    def embed_documents(docs, collection_name):
        text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=150)
        texts = text_splitter.split_documents(docs)
        vectordb = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR,
            client=client
        )
        vectordb.add_documents(texts)

    def get_collections():
        return [c.name for c in client.list_collections()]

    # UI Principal
    st.header("📂 Consulta de Documentos (RAG)")

    with st.sidebar:
        st.markdown("### 📁 Gestão de Coleções")
        new_name = st.text_input("Criar nova coleção")
        if st.button("➕ Criar Coleção") and new_name:
            client.create_collection(name=new_name)
            st.success(f"Coleção '{new_name}' criada!")

        collections = get_collections()
        selected_collection = st.selectbox(
            "Selecionar coleção", collections if collections else ["Nenhuma coleção"])

        if selected_collection and selected_collection != "Nenhuma coleção":
            if "vectordb" not in st.session_state or st.session_state.get("current_collection") != selected_collection:
                vectordb = Chroma(
                    collection_name=selected_collection,
                    embedding_function=embeddings,
                    persist_directory=CHROMA_DIR,
                    client=client
                )
                st.session_state.vectordb = vectordb
                st.session_state.current_collection = selected_collection
                st.session_state.messages = []  # Limpar chat ao trocar de coleção

        uploaded_files = st.file_uploader("Upload de documentos", type=[
                                          "pdf", "docx"], accept_multiple_files=True)
        if uploaded_files and selected_collection and st.button("📥 Inserir documentos"):
            os.makedirs("temp_uploads", exist_ok=True)
            all_docs = []
            for file in uploaded_files:
                docs = load_document(file)
                if docs:
                    all_docs.extend(docs)
            embed_documents(all_docs, selected_collection)
            st.success(
                f"Documentos adicionados à coleção '{selected_collection}'.")

    # CHAT RAG
    if "vectordb" in st.session_state:
        retriever = st.session_state.vectordb.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 10, "fetch_k": 100}
        )

        prompt_template = ChatPromptTemplate.from_template("""
        Human: És um assistente de IA especializado em analisar e extrair informações de vários documentos de propostas de serviços. O teu objetivo é fornecer respostas rigorosas, concisas e baseadas em factos, dando prioridade a dados numéricos e estatísticas sempre que possível.

        Utiliza apenas a informação relevante dos documentos fornecidos, ignorando qualquer contexto que não esteja diretamente relacionado com a pergunta. Se a resposta não estiver nos documentos, indica claramente que não tens informação suficiente em vez de fazer suposições.

        Indica sempre o(s) ficheiro(s) de origem de onde retiraste a informação.

        <contexto>  
        {context}  
        </contexto>  

        <pergunta>  
        {question}  
        </pergunta>  

        Histórico da Conversa Anterior:
        {conversation_history}

        Instruções:  
        - Pesquisa em vários documentos para encontrar os dados relevantes.  
        - Elimina informação que não esteja diretamente relacionada com a pergunta.  
        - Sempre que possível, inclui números, datas, percentagens ou outros detalhes concretos.  
        - Lista o(s) nome(s) dos ficheiros de onde extraíste as respostas.

        Assistente:  
        """)

        # Seleção de modelo
        model = ChatOpenAI(temperature=0, model="gpt-4o-mini", stream=True)
        # model = OllamaLLM(temperature=0, model="llama3:8b", base_url="http://192.168.0.3:11434", stream=True)

        chain = (
            {
                "context": RunnableLambda(lambda x: retriever.invoke(x["question"])),
                "question": RunnablePassthrough(),
                "conversation_history": RunnablePassthrough()
            }
            | prompt_template
            | model
            | StrOutputParser()
        )

        # Inicializar histórico se necessário
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Renderizar histórico
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input do utilizador
        if user_input := st.chat_input("Escreva a sua pergunta..."):
            # Adicionar pergunta
            st.session_state.messages.append(
                {"role": "user", "content": user_input})

            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                dots_placeholder = st.empty()

                # Animação de loading enquanto gera resposta
                for i in range(3):
                    dots_placeholder.markdown(f"🔄 A pensar{'.' * (i % 4)}")
                    time.sleep(0.5)

                # Gerar resposta real
                full_response = ""
                for chunk in chain.stream({
                    "question": user_input,
                    "conversation_history": "\n".join(
                        [m["content"]
                            for m in st.session_state.messages if m["role"] == "user"]
                    )
                }):
                    full_response += chunk
                    placeholder.markdown(full_response)

                dots_placeholder.empty()
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response})
