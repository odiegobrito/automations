import fitz  # PyMuPDF
import re
import os

# Função para extrair e salvar imagens com o nome do GTIN
def extract_images_with_gtin(pdf_path, output_folder):
    # Verifica se a pasta de saída existe, caso contrário, cria
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Abre o PDF
    pdf_document = fitz.open(pdf_path)
    gtin_map = {}  # Dicionário para mapear GTINs com imagens

    # Percorre as páginas do PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        # Extrai o texto da página
        text = page.get_text()
        
        # Captura todos os GTINs com 12 a 14 dígitos na página
        gtin_matches = re.findall(r'GTIN\s*:\s*(\d{6,10})', text)
        if gtin_matches:
            for gtin in gtin_matches:
                # Para cada GTIN encontrado, associar imagens
                gtin_map[gtin] = []
                
            # Extrai as imagens na página
            image_list = page.get_images(full=True)
            if image_list:
                for img_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Seleciona o GTIN atual para a imagem (ou usa o último GTIN encontrado)
                    current_gtin = gtin_matches[min(img_index-1, len(gtin_matches)-1)]
                    
                    # Gera o nome do arquivo para cada GTIN e imagem
                    image_filename = os.path.join(output_folder, f"{current_gtin}.png")
                    unique_index = 1
                    while os.path.exists(image_filename):
                        image_filename = os.path.join(output_folder, f"{current_gtin}_{unique_index}.png")
                        unique_index += 1
                    
                    # Salva a imagem no diretório
                    with open(image_filename, "wb") as image_file:
                        image_file.write(image_bytes)
                        print(f"Imagem salva como {image_filename}")
                    
                    # Associa a imagem ao GTIN
                    gtin_map[current_gtin].append(image_filename)

    pdf_document.close()
    print("Processamento concluído.")
    return gtin_map  # Retorna o mapeamento de GTINs e imagens para verificação

# Uso da função
pdf_path = "D:/Projects/python-extrair/dadiva.pdf"  # Caminho para o arquivo PDF
output_folder = "D:\Projects\python-extrair\Extraidas"  # Pasta de saída para as imagens
gtin_images_map = extract_images_with_gtin(pdf_path, output_folder)

# Exibe o mapeamento de GTINs e imagens salvas para verificação
for gtin, images in gtin_images_map.items():
    print(f"GTIN {gtin} possui as imagens: {images}")
