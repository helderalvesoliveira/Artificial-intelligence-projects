from crewai import Agent, Task, Crew, Process, LLM
import textwrap
import re
import os
from dotenv import load_dotenv
load_dotenv(override=True)

CHROMA_DIR = "./chroma_db"
OUTPUT_FILE = "ata_reuniao.txt"

# LLM setup
llm = LLM(
    model=os.getenv('MODEL'),
    temperature=0.3,
    max_tokens=8192,
    stream=True
)

summary_agent = Agent(
    role="Especialista em Atas de Reunião",
    goal="Produzir atas detalhadas, com os tópicos discutidos, decisões tomadas e ações atribuídas",
    backstory=(
        "És um especialista com vasta experiência em reuniões empresariais. "
        "Tens um olho clínico para identificar pontos essenciais e transformar conversas "
        "em atas organizadas e acionáveis. O teu trabalho é essencial para garantir o seguimento das decisões."
    ),
    llm=llm,
    verbose=False
)

# Funções auxiliares
def extract_date(text):
    patterns = [
        r'(\d{1,2} [A-Za-z]+ \d{4}, \d{1,2}:\d{2}(?:am|pm)?)',
        r'([A-Za-z]+, \d{1,2} [A-Za-z]+ \d{4}, \d{1,2}:\d{2}(?:am|pm)?)',
        r'(\d{2}/\d{2}/\d{4} \d{1,2}:\d{2})',
        r'(\d{4}-\d{2}-\d{2} \d{1,2}:\d{2})',
        r'Date: (\d{2}/\d{2}/\d{4})\s*Time: (\d{1,2}:\d{2})'
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}" if len(match.groups()) == 2 else match.group(1)
    return None

def split_text(texto, max_len=2000):
    return textwrap.wrap(texto, max_len, break_long_words=False, replace_whitespace=False)

# Função principal de resumo
def resume_transcription(texto, listener=None):
    partes = split_text(texto)
    data_hora = extract_date(texto)
    print(f"🔹 Data e hora extraídas: {data_hora}")
    resumos = []

    # ✅ Limpa o ficheiro no início
    with open(OUTPUT_FILE, "w", encoding="utf-8") as ata:
        ata.write("")
        if data_hora:
            ata.write(f"Data da reunião: {data_hora}\n\n")

    # Processa e salva resumos parciais
    for i, parte in enumerate(partes):
        print(f"🔹 Resumindo parte {i+1}/{len(partes)}")
        tarefa = Task(
            description=(
                "Você receberá um trecho de uma transcrição de reunião. "
                "Produza um resumo objetivo (3–5 frases)focado no mais relevante. "
                "Não incluas o pontos principais, uma vez que se trata de um trecho e terá mais partes. "
                "Evite repetições ou introduções genéricas.\n\n" + parte
            ),
            expected_output="Sumarização concisa.",
            agent=summary_agent
        )
        crew = Crew(agents=[summary_agent], tasks=[tarefa], process=Process.sequential, event_listener=listener)
        output = crew.kickoff()
        if output and hasattr(output, "raw"):
            resumo_limpo = output.raw.strip()
            resumos.append(resumo_limpo)
            with open(OUTPUT_FILE, "a", encoding="utf-8") as ata:
                ata.write(resumo_limpo + "\n\n")

    # Gera o resumo final
    tarefa_final = Task(
        description=(
            "A seguir há resumos parciais de uma reunião. Unifique‑os num resumo "
            "final coeso, organizado em tópicos e bullet points para decisões e próximas ações. "
            "Evite repetições e mantenha a ordem cronológica dos temas.\n\n" + "\n".join(resumos)
        ),
        expected_output="Ata da reunião, com tópicos‑chave, decisões e tarefas atribuídas.",
        agent=summary_agent,
    )
    crew_final = Crew(agents=[summary_agent], tasks=[tarefa_final], process=Process.sequential)
    resultado_final = crew_final.kickoff()

    # Adiciona o resumo final ao final do ficheiro
    with open(OUTPUT_FILE, "a", encoding="utf-8") as ata:
        ata.write("Resumo final da reunião:\n")
        ata.write(resultado_final.raw.strip() + "\n")

    return resultado_final.raw.strip()
