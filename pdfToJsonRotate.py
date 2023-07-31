import json
import io
import os
import pytesseract
import cv2
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import numpy as np


# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' 
tessdata_dir_config = '--tessdata-dir "/usr/share/tesseract-ocr/5/tessdata" -l spa'

# Ruta a la carpeta raíz de los PDFs
root_folder = '/home/alex/pdfs/'


# Función para preprocesar la imagen antes de pasarla por el OCR
def preprocess_image(image):
    # Aplica un filtro de mediana para reducir el ruido
    image = cv2.medianBlur(image, 5)
    # Convierte la imagen a escala de grises
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Binarización adaptativa para convertir la imagen a blanco y negro
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Aplica un suavizado gaussiano para reducir el ruido
    image = cv2.GaussianBlur(image, (3,3), 0)
    # Enderezamiento del texto
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return image


# Función para rotar un archivo PDF y escanearlo
def rotate_and_scan_pdf(pdf_path):
    pdf_name, pdf_ext = os.path.splitext(os.path.basename(pdf_path))

    # Leer el archivo PDF
    pdf_reader = PdfReader(pdf_path)
    num_pages = len(pdf_reader.pages)

    # Crear una instancia de PdfWriter para guardar el PDF rotado
    pdf_writer = PdfWriter()

    # Rotar el PDF y guardar las páginas rotadas en pdf_writer
    for page in pdf_reader.pages:
        rotated_page = page.rotate(-90)  # Rotar 90º a la izquierda
        pdf_writer.add_page(rotated_page)

    # Guardar el PDF rotado en un nuevo archivo
    rotated_pdf_path = os.path.join(os.path.dirname(pdf_path), f"{pdf_name}_rotado.pdf")
    with open(rotated_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

    # Convierte el PDF rotado a una lista de imágenes
    rotated_pages = convert_from_path(rotated_pdf_path, 300)

    # Procesa cada página con Tesseract OCR y extrae el texto
    text = []
    for idx, page in enumerate(rotated_pages):
        img_byte_arr = io.BytesIO()
        page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        # Convierte la imagen a un array de Numpy para poder preprocesarla
        nparr = np.frombuffer(img_byte_arr, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = preprocess_image(image)
        # Convierte la imagen preprocesada a un objeto PIL para pasarla por el OCR
        img_pil = Image.fromarray(image)
        page_text = pytesseract.image_to_string(img_pil, lang='spa', config=tessdata_dir_config)
        text.append(page_text)

    # Convierte el texto en un objeto JSON estructurado
    json_obj = {}
    for idx, page in enumerate(text):
        json_obj[f"Page {idx+1}"] = page.strip().split('\n')

    # Guarda el objeto JSON en un archivo en la misma carpeta que el archivo PDF original
    output_path = os.path.join(os.path.dirname(pdf_path), f"{pdf_name}_rotado.json")
    with open(output_path, 'w') as outfile:
        json.dump(json_obj, outfile, ensure_ascii=False, indent=4)
    
    # Crear archivo de salida en formato TXT
    output_txt_path = os.path.join(root, f"{pdf_name}_rotado.txt")
    with open(output_txt_path, 'w') as f:
        for page in json_obj.keys():
            for line in json_obj[page]:
                f.write(f"file: '{pdf_name}_rotado.json' page {page}, line {line}\n")

# Recorre todos los archivos PDF en la carpeta raíz y sus subcarpetas
for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file.lower().endswith('.pdf'):
            # Obtiene la ruta completa del archivo
            pdf_path = os.path.join(root, file)
            # Llama a la función rotate_and_scan_pdf para procesar el archivo
            rotate_and_scan_pdf(pdf_path)