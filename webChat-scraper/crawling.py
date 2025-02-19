import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin  # Para manipular links relativos
from dotenv import load_dotenv, find_dotenv
import os

class ScrapeSpider(scrapy.Spider):
    load_dotenv(find_dotenv())
    name = os.getenv('NAME_URL_SCRAPING')
    start_urls = [os.getenv('URL_SCRAPING')]

    def parse(self, response):
        # Extrair links e converter para URLs absolutas
        raw_links = response.css("a::attr(href)").getall()
        links = [urljoin(response.url, link) for link in raw_links if link]

        # Consolidar dados em um único dicionário
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "h1": response.css("h1::text").getall(),
            "links": links,
        }

# Configurar o processo do Scrapy
process = CrawlerProcess(settings={
    "FEEDS": {"output.json": {"format": "json", "overwrite": True}},  # Substitui conteúdo
    "LOG_LEVEL": "INFO",  # Configuração do log
})


process.crawl(ScrapeSpider)
process.start()
