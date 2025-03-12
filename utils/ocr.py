import cv2
import pytesseract
from pytesseract import Output
from config.settings import TESSERACT_PATH

# Configura o caminho do Tesseract OCR
pytesseract.tesseract_cmd = TESSERACT_PATH

def read_text_from_image(image_path, lang='por'):
    """
    Lê texto de uma imagem usando OCR (Tesseract).
    :param image_path: Caminho da imagem contendo o texto.
    :param lang: Idioma do texto (padrão: 'por' para português).
    :return: Texto extraído da imagem.
    """
    try:
        # Carrega a imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Imagem não encontrada: {image_path}")

        # Converte a imagem para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplica OCR
        text = pytesseract.image_to_string(gray, lang=lang)
        return text.strip()  # Remove espaços em branco no início e no fim
    except Exception as e:
        print(f"Erro ao ler texto da imagem: {e}")
        return None

def read_numbers_from_image(image_path):
    """
    Lê apenas números de uma imagem usando OCR (Tesseract).
    :param image_path: Caminho da imagem contendo os números.
    :return: Números extraídos da imagem.
    """
    try:
        # Carrega a imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Imagem não encontrada: {image_path}")

        # Converte a imagem para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplica OCR com configuração para reconhecer apenas números
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        text = pytesseract.image_to_string(gray, config=custom_config)
        return text.strip()  # Remove espaços em branco no início e no fim
    except Exception as e:
        print(f"Erro ao ler números da imagem: {e}")
        return None

def get_text_position(image_path, text_to_find, lang='por'):
    """
    Encontra a posição de um texto específico em uma imagem.
    :param image_path: Caminho da imagem.
    :param text_to_find: Texto a ser procurado.
    :param lang: Idioma do texto (padrão: 'por' para português).
    :return: Coordenadas (x, y) do texto encontrado ou None.
    """
    try:
        # Carrega a imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Imagem não encontrada: {image_path}")

        # Converte a imagem para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplica OCR e obtém os dados de saída
        data = pytesseract.image_to_data(gray, lang=lang, output_type=Output.DICT)

        # Procura o texto na saída do OCR
        for i, text in enumerate(data['text']):
            if text_to_find.lower() in text.lower():
                x = data['left'][i]
                y = data['top'][i]
                return (x, y)
        return None
    except Exception as e:
        print(f"Erro ao encontrar a posição do texto: {e}")
        return None