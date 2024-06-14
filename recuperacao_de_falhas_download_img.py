import os
import requests
import re
import crawler

file_path = 'urls.txt' # Adjust as needed
results = crawler.read_file(file_path)

"""for result in results:
    print(result["id_product"])
    print(result["urls_retornadas"])"""

# Create main directory for images if it doesn't exist
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
