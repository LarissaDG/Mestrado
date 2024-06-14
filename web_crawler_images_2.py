from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import os
import requests

# Caminho para o arquivo CSV
csv_path = "/mnt/c/Users/Dell/Documents/Escola/UFMG/Mestrado/Monografia/Mestrado/Dados/zara.csv"

# Carregar dados do CSV
dados = pd.read_csv(csv_path, sep=';')
df = dados
print(df.head())

# Pegar as URLs e IDs dos produtos
urls = df["url"].tolist()
id_products = df["Product ID"].tolist()

def crawler(url):
    # Inicializa variavel imagens
    list_img_link = []
    
    # Caminho para o geckodriver (substitua pelo caminho correto no seu sistema)
    gecko_driver_path = '/mnt/c/Users/Dell/Downloads/geckodriver-v0.34.0-win64/geckodriver.exe' 

    # Configurando as opções do Firefox
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Executar no modo headless
    firefox_options.add_argument('--disable-gpu')  # Desabilitar GPU
    firefox_options.add_argument('--disable-popup-blocking')  # Desabilitar bloqueio de pop-ups

    # Configurando o serviço do geckodriver
    service = Service(executable_path=gecko_driver_path)

    # Inicializando o webdriver do Firefox com as opções configuradas
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # Acessando a página com Selenium
    driver.get(url)

    # Esperando alguns segundos para garantir que a página seja carregada completamente
    time.sleep(5)

    # Obtendo o conteúdo da página
    page_content = driver.page_source

    # Analisando o conteúdo da página com BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')

    # Encontrando o script com o JSON-LD que contém os dados do produto
    json_ld_script = soup.find('script', type='application/ld+json')
    if json_ld_script:
        # Carregando o JSON-LD
        json_ld_content = json.loads(json_ld_script.string)
        
        # Verificando se o JSON-LD é uma lista
        if isinstance(json_ld_content, list):
            # Extraindo as URLs das imagens
            img_urls = [item['image'] for item in json_ld_content if 'image' in item]
            
            # Exibindo os URLs das imagens encontradas
            for img_url in img_urls:
                print(img_url)
                list_img_link.append(img_url)
        else:
            print("O JSON-LD não é uma lista.")
    else:
        print("O script JSON-LD não foi encontrado.")

    # Fechando o driver do Selenium
    driver.quit()

    return list_img_link

# Função para baixar imagens
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar {url}: {e}")

# Estrutura de dados para armazenar os resultados
resultados = []

# Para cada URL na lista, execute o crawler e armazene os resultados
for url, id_product in zip(urls, id_products):
    urls_retornadas = crawler(url)
    resultados.append({
        "original_url": url,
        "id_product": id_product,
        "urls_retornadas": urls_retornadas
    })

    # Criar pasta para o id_product se não existir
    os.makedirs(id_product, exist_ok=True)
    
    # Baixar cada imagem na pasta correspondente
    for img_url in urls_retornadas:
        # Nome do arquivo baseado na URL da imagem
        img_name = img_url.split("/")[-1]
        save_path = os.path.join(id_product, img_name)
        download_image(img_url, save_path)

# Exibir a estrutura de dados resultante
print(resultados)
