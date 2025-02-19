import json
import os
import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv(override=True)
# Carregar o JSON com os links extraídos
with open("output.json", "r") as f:
    data = json.load(f)

# Extraindo links únicos e filtrar apenas os do domínio desejado
base_url = os.getenv('URL_SCRAPING')
links = set()  # Usar um set para evitar duplicados
for entry in data:
    for link in entry["links"]:
        print(link)
        if link.startswith(base_url):  # Filtrar links do domínio desejado
            links.add(link)

print(f"Total de links únicos para processar: {len(links)}")

# Função para processar cada URL
def fetch_url(url, retries=3):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Extrair título
                title = soup.title.string.strip() if soup.title else "Sem título"
                
                # Extrair conteúdo da página
                content = soup.get_text(separator=" ").strip()
                content = " ".join(content.split())[:5000]  # Limitar para 5000 caracteres
                
                # Extrair links (href)
                page_links = [a.get('href') for a in soup.find_all('a', href=True)]
                page_links = list(set(page_links))  # Remover duplicados
                
                return {
                    "url": url,
                    "title": title,
                    "content": content,
                    "links": "; ".join(page_links)  # Concatenar links com separador
                }
        except Exception as e:
            with open("errors.log", "a", encoding="utf-8") as error_log:
                error_log.write(f"Erro ao processar {url}: {e}\n")
    return None

# Processar URLs em paralelo usando ThreadPoolExecutor
scraped_data = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(tqdm(executor.map(fetch_url, links), total=len(links)))
    scraped_data = [result for result in results if result]  # Filtrar resultados válidos

# Guardar os dados extraídos em um arquivo CSV
with open("scraped_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["url", "title", "content", "links"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(scraped_data)

print("Dados salvos em scraped_data.csv")
