import cv2
import numpy as np
import pyautogui
from config.settings import TESSERACT_PATH, MONSTERS_DIR
from pytesseract import pytesseract

# Configura o caminho do Tesseract OCR
pytesseract.tesseract_cmd = TESSERACT_PATH

def find_image_on_screen(image_path, threshold=0.8):
    """
    Procura uma imagem na tela usando OpenCV.
    :param image_path: Caminho da imagem a ser procurada.
    :param threshold: Limiar de confiança para a detecção (0 a 1).
    :return: Coordenadas (x, y) da imagem encontrada ou None.
    """
    try:
        # Captura a tela
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Carrega a imagem de referência
        template = cv2.imread(image_path, 0)
        if template is None:
            raise ValueError(f"Imagem não encontrada: {image_path}")

        # Realiza a correspondência de template
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Verifica se a correspondência está acima do limiar
        if max_val >= threshold:
            return max_loc  # Retorna as coordenadas (x, y) da imagem encontrada
        return None
    except Exception as e:
        print(f"Erro ao procurar imagem: {e}")
        return None

def find_monster_on_screen(monster_name, threshold=0.8):
    """
    Procura um monstro na tela com base em seus sprites.
    :param monster_name: Nome do monstro (ex: "agressor", "aquecedor").
    :param threshold: Limiar de confiança para a detecção (0 a 1).
    :return: Coordenadas (x, y) do monstro encontrado ou None.
    """
    # Define os sprites do monstro
    if monster_name == "agressor":
        sprites = [f"{MONSTERS_DIR}agressor_{i}.png" for i in range(1, 5)]
    elif monster_name == "aquecedor":
        sprites = [f"{MONSTERS_DIR}aquecedor_{i}.png" for i in range(1, 9)]
    elif monster_name == "congelador":
        sprites = [f"{MONSTERS_DIR}congelador_{i}.png" for i in range(1, 5)]
    elif monster_name == "batedor":
        sprites = [f"{MONSTERS_DIR}batedor_{i}.png" for i in range(1, 5)]
    else:
        raise ValueError(f"Monstro desconhecido: {monster_name}")

    # Procura por qualquer sprite do monstro na tela
    for sprite in sprites:
        location = find_image_on_screen(sprite, threshold)
        if location:
            return location
    return None

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