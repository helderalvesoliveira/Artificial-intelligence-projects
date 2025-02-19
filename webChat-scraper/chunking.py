import pandas as pd
import textwrap

df = pd.read_csv("scraped_data.csv")

# Configurar o tamanho do chunk (ajustável conforme o modelo)
chunk_size = 500  # Aproximado em número de palavras, ajustável

# Função para dividir o texto em chunks
def chunk_text(text, size):
    """
    Divide um texto em chunks de tamanho `size`.
    """
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i + size])

# Criar uma lista para armazenar os chunks
chunked_data = []

# Iterar pelas linhas do CSV e dividir o conteúdo em chunks
for index, row in df.iterrows():
    url = row["url"]
    title = row["title"]
    content = row["content"]
    
    # Dividir o conteúdo em chunks
    for i, chunk in enumerate(chunk_text(content, chunk_size)):
        chunked_data.append({
            "url": url,
            "title": title,
            "chunk_id": i + 1,
            "chunk_content": chunk
        })

# Criar um DataFrame com os chunks
chunked_df = pd.DataFrame(chunked_data)

# Salvar os chunks em um novo CSV (opcional)
chunked_df.to_csv("chunked_data.csv", index=False, encoding="utf-8")

print("Dados divididos em chunks e salvos em 'chunked_data.csv'")
