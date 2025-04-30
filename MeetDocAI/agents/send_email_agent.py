# main.py
import os
from crewai import Agent, Task, Crew, Process, LLM
from tools.send_email_tool import enviar_email_tool
from dotenv import load_dotenv
import json

load_dotenv(override=True)

llm = LLM(
    model=os.getenv('MODEL'),
    temperature=0.3,
    max_tokens=8192,
    stream=True
)

# Define o agente
email_agent = Agent(
    role="Agente de Envio de Email",
    goal="Enviar atas de reunião com sucesso para os destinatários.",
    backstory="Este agente é responsável por comunicações oficiais da empresa via email.",
    tools=[enviar_email_tool],
    verbose=True,
    llm=llm
)


email = os.getenv("RESEND_EMAIL")
caminho = os.getenv("PATH_ATA")

if not email or not caminho:
    raise ValueError("Variáveis de ambiente RESEND_EMAIL ou PATH_ATA não estão definidas.")

params = {
    "destinatario": email,
    "caminho_ficheiro": caminho,
}

json_str = json.dumps(params)

tarefa_email = Task(
    description=(
        "Use a ferramenta Enviar Email com a json string:\n"
        f"{json_str}\n"
        "para enviar a ata da reunião como anexo para o destinatário."
    ),
    expected_output="Confirmação de que o email foi enviado com sucesso.",
    agent=email_agent
)
# Cria e executa a crew
crew = Crew(
    agents=[email_agent],
    tasks=[tarefa_email],
    process=Process.sequential,
    verbose=True
)

