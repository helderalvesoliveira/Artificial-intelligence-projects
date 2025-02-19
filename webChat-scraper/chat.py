import streamlit as st
import os
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain_community.chat_models import ChatOllama

def check_retriever(retriever, user_input):
    # 1) Usar os documentos relevantes para a pergunta
    retrieved_docs = retriever.get_relevant_documents(user_input)

    # 2) Mostrar no console ou no Streamlit quais documentos foram retornados
    print("Documentos retornados pelo retriever:")
    for i, doc in enumerate(retrieved_docs, start=1):
        print(f"Doc {i}:")
        print("---------- page_content ----------")
        print(doc.page_content[:200], "...")
        print("---------- metadata --------------")
        print(doc.metadata)
        print("----------------------------------\n")

    # Retorna os documentos recuperados
    return retrieved_docs

def build_context_with_history(retrieved_docs, history):
    # Combina os documentos retornados pelo retriever
    context_docs = "\n".join([doc.page_content for doc in retrieved_docs])

    # Combina o histórico de mensagens no formato desejado
    history_context = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]
    )

    # Retorna o contexto final, incluindo documentos e histórico
    return f"{context_docs}\n\nHistórico:\n{history_context}"

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Definir o modelo ChatGroq a ser usado
model_local = ChatGroq(model="llama-3.3-70b-versatile")
#model_local = ChatOllama(model="llama3.1:8b",base_url=os.getenv("OLLAMA_SERVER_URL"))
@st.cache_resource
def load_csv_data(csv_path: str = "scraped_data.csv"):
    """Carrega dados a partir de um CSV, divide em chunks e cria a base para o retriever."""
    df = pd.read_csv(csv_path)
    
    # Verifica existência da coluna 'content'
    if "content" not in df.columns:
        print("ERRO: a coluna 'content' não está presente no CSV!")
        return None

    documents = []
    for idx, row in df.iterrows():
        text_content = str(row["content"]) 
        if not text_content or text_content.strip() == "":
            print(f"A linha {idx} está vazia na coluna 'content'.")

        metadata = {"row_index": idx, "url": row["url"]}
        doc = Document(page_content=text_content, metadata=metadata)
        documents.append(doc)

    # Divide os documentos em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitted_docs = text_splitter.split_documents(documents)

    if len(splitted_docs) == 0:
        print("Nenhum documento válido para criar embeddings. Verifique o CSV.")
        return None

    # Cria embeddings e vetoriza
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    #embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splitted_docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})  # Número de documents a retornar
    return retriever

retriever = load_csv_data()

# Título do app
st.title("Assistente Virtual de Website")

# Template do prompt RAG
rag_template = """
És um(a) assistente virtual de um website, com acesso a toda a informação relevante da empresa, incluindo **serviços**, **áreas de atuação** e outros dados essenciais para apoio ao cliente. O teu papel é responder de forma clara, objetiva e profissional, baseando-te sempre no **contexto fornecido**. Segue estas orientações:

1. **Idioma**:  
   - Responde no mesmo idioma da pergunta.  
   - Se a pergunta estiver em português, utiliza **Português de Portugal**, evitando o "você", o gerúndio e expressões do português do Brasil.

2. **Saudação**:  
   - Cumprimenta o utilizador apenas na **primeira interação**, de forma formal e profissional.  
   - Nas respostas seguintes, evita saudações ou introduções longas e segue diretamente para o conteúdo relevante.

3. **Respostas Concisas**:  
   - Responde **diretamente ao que foi perguntado**, sem repetir desnecessariamente informações já mencionadas na interação anterior.  
   - Sempre que necessário, complementa a resposta com informações adicionais relevantes, mas evita copiar e colar trechos extensos de conteúdo de forma repetitiva.  

4. **Restrições**:  
   - Responde apenas com base no **contexto fornecido**. Se não encontrares a resposta no contexto, indica de forma educada que não dispões dessa informação.  

5. **Estilo**:  
   - Mantém a resposta objetiva, formal e focada no que o cliente procura.  
   - Evita repetições desnecessárias de conteúdos ou introduções.  

**Contexto**: {context}  

**Pergunta do cliente**: {question}
"""



prompt = ChatPromptTemplate.from_template(rag_template)

# Construção do "chain" RAG (Retrieval-Augmented Generation)
chain = (
    {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
    | prompt
    | model_local
)

# -----------------------------------------------------------------------------------
# Sessão: Histórico, contadores e flags
# -----------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # Armazena o histórico de mensagens
        # Adiciona uma saudação inicial
    initial_greeting = {
        "role": "assistant",
        "content": (
            "Olá! Bem-vindo(a). Sou o seu assistente virtual e estou aqui para ajudar. "
            "Por favor, escreva a sua pergunta ou dúvida e farei o meu melhor para fornecer uma resposta precisa."
        )
    }
    st.session_state.messages.append(initial_greeting)

if "user_question_count" not in st.session_state:
    st.session_state.user_question_count = 0  # Contador de perguntas do utilizador

# -----------------------------------------------------------------------------------
# Mostra mensagens do histórico (tanto user como assistant)
# -----------------------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------------------------------------------------------
# Caixa de entrada do utilizador
# -----------------------------------------------------------------------------------
user_input = st.chat_input("Escreva a sua pergunta aqui...")

if user_input:
    # Contador de perguntas do utilizador
    st.session_state.user_question_count += 1

    # Regista a pergunta do utilizador no histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Se há um retriever carregado, faz a pesquisa de documentos
    if retriever:
        retrieved_docs = check_retriever(retriever, user_input)
        full_context = build_context_with_history(retrieved_docs, st.session_state.messages)
    else:
        # Se não temos retriever, não conseguimos RAG
        full_context = "Sem documentos para contexto."

    # Chama a pipeline do modelo
    response_stream = chain.stream({"context": full_context, "question": user_input})
    full_response = ""

    response_container = st.chat_message("assistant")
    response_text = response_container.empty()

    # Faz o streaming da resposta do modelo
    for partial_response in response_stream:
        full_response += str(partial_response.content)
        response_text.markdown(full_response + "▌")

    # Mostra a resposta final (sem o cursor "▌")
    response_text.markdown(full_response)
    # Guarda no histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
