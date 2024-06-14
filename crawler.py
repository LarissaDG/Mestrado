from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests
import os

def crawler(url):
    # Inicializa variável imagens
    list_img_link = set()  # Usando set para evitar duplicatas
    
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
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            # Carregando o JSON-LD
            json_ld_content = json.loads(script.string)
            
            # Verificando se o JSON-LD é uma lista ou um dicionário
            if isinstance(json_ld_content, list):
                # Extraindo as URLs das imagens
                for item in json_ld_content:
                    if 'image' in item:
                        if isinstance(item['image'], list):
                            img_urls = item['image']
                        else:
                            img_urls = [item['image']]
                        list_img_link.update(img_urls)
            elif isinstance(json_ld_content, dict):
                if 'image' in json_ld_content:
                    if isinstance(json_ld_content['image'], list):
                        img_urls = json_ld_content['image']
                    else:
                        img_urls = [json_ld_content['image']]
                    list_img_link.update(img_urls)
        except json.JSONDecodeError:
            continue

    # Adicionalmente, procurar por tags <img> e extrair URLs das imagens
    img_tags = soup.find_all('img', class_='media-image__image')
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            list_img_link.add(img_url)

    # Fechando o driver do Selenium
    driver.quit()

    return list(list_img_link)  # Convertendo de volta para lista

import requests
import time

# Função para baixar imagens com retry e backoff
def download_image(url, save_path, retries=5, backoff_factor=1.0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Verifica se houve um erro HTTP
            
            # Salvar o conteúdo se a solicitação for bem-sucedida
            with open(save_path, 'wb') as file:
                file.write(response.content)
            return  # Sucesso, saia da função

        except requests.exceptions.HTTPError as e:
            # Tratar especificamente erro 404
            if response.status_code == 404:
                print(f"Erro 404: {url} não encontrado. Pulando download.")
                return
            else:
                print(f"Erro HTTP ao baixar {url}: {e}")
        except requests.exceptions.SSLError as e:
            print(f"Erro SSL ao baixar {url}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar {url}: {e}")
        
        # Aguarde um tempo antes de tentar novamente
        sleep_time = backoff_factor * (2 ** i)  # Exponential backoff
        print(f"Aguardando {sleep_time} segundos antes de tentar novamente...")
        time.sleep(sleep_time)
    
    print(f"Falha ao baixar {url} após {retries} tentativas")

# Function to read the file and extract id_product and urls_retornadas
def read_file(file_path):
    resultados = []

    with open(file_path, 'r') as file:
        id_product = None
        urls_retornadas = []

        while True:
            line = file.readline()
            if not line:
                break
            if line.startswith("Id:"):
                if id_product is not None:
                    resultados.append({
                        "id_product": id_product,
                        "urls_retornadas": urls_retornadas
                    })
                    urls_retornadas = []

                id_product = line.split(":")[1].strip()
            elif line.startswith("Images url:"):
                continue
            else:
                urls_retornadas.append(line.strip())

        if id_product is not None:
            urls_retornadas = set(urls_retornadas) #TODO corrigir
            resultados.append({
                "id_product": id_product,
                "urls_retornadas": urls_retornadas
            })

    return resultados
