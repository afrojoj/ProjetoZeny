import os

# Diretórios das imagens
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
MONSTERS_DIR = os.path.join(ASSETS_DIR, "monsters")
UI_ELEMENTS_DIR = os.path.join(ASSETS_DIR, "ui_elements")
CAPTCHA_DIR = os.path.join(ASSETS_DIR, "captcha")
MAPS_DIR = os.path.join(ASSETS_DIR, "maps")

# Configurações de OCR
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Insira o caminho do Tesseract

# Configurações de tempo
WAIT_TIME = 0.5  # Tempo de espera padrão
RANDOM_DELAY = (0.1, 0.3)  # Aleatorização de tempo