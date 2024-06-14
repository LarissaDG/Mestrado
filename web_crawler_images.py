import pandas as pd
import crawler
import os

# Caminho para o arquivo CSV
csv_path = "/mnt/c/Users/Dell/Documents/Escola/UFMG/Mestrado/Monografia/Mestrado/Dados/zara.csv"

# Carregar dados do CSV
dados = pd.read_csv(csv_path, sep=';')
df = dados
print(df.head())

# Pegar as URLs e IDs dos produtos
urls = df["url"].tolist()
id_products = df["Product ID"].tolist()

# Estrutura de dados para armazenar os resultados
resultados = []

print("Processando ...")
count = 0 
# Para cada URL na lista, execute o crawler e armazene os resultados
for url, id_product in zip(urls, id_products):
    urls_retornadas = crawler.crawler(url)
    urls_retornadas = list(set(urls_retornadas))  # Remover duplicatas
    resultados.append({
        "original_url": url,
        "id_product": id_product,
        "urls_retornadas": urls_retornadas
    })
    print(count)
    count += 1 

    # Exibir a estrutura de dados resultante
    with open('out.txt', 'a') as f:
        f.write("Id:" + str(id_product) + "\n")
        f.write("Images url:\n")
        for item in urls_retornadas:
            f.write(f"{item}\n")
    f.close()

print(resultados)
print("Arquivo finalizado")

print("Inicio baixar imagens")
base_directory = "Imagens"
os.makedirs(base_directory, exist_ok=True)

for result in results:
    id_product = result["id_product"]
    urls_retornadas = result["urls_retornadas"]

    # Create subdirectory for each id_product if it doesn't exist
    product_directory = os.path.join(base_directory, id_product)
    os.makedirs(product_directory, exist_ok=True)

    print(f"Início baixar imagens para {id_product}")
    count = 0
    # Baixar cada imagem na pasta correspondente
    for img_url in urls_retornadas:
        #print(img_url)
        # Extracting file name from URL and removing query parameters
        img_name_with_params = img_url.split("/")[-1]
        img_name, _ = img_name_with_params.split("?", 1) if "?" in img_name_with_params else (img_name_with_params, "")

        # Ensuring file extension is ".jpg"
        if not img_name.lower().endswith(".jpg"):
            img_name += ".jpg"

        # Cleaning up image name
        img_name = re.sub(r'[^\w\-_.]', '', img_name)

        # Save path with corrected file name
        save_path = os.path.join(product_directory, img_name)

        crawler.download_image(img_url, save_path)

        print(count)
        count += 1

    print(f"Todas as imagens para {id_product} foram baixadas")
    print("===")

print("Arquivo finalizado")

