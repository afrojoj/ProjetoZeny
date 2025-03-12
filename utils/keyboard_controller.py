import time
import random
import pyautogui
from config.settings import RANDOM_DELAY
from config.hotkeys import HOTKEYS

def press_hotkey(hotkey):
    """
    Pressiona uma tecla ou combinação de teclas.
    :param hotkey: Tecla ou combinação de teclas (ex: 'f1', 'ctrl+shift+a').
    """
    try:
        pyautogui.hotkey(*hotkey.split('+'))  # Divide a hotkey em partes (ex: 'ctrl+shift+a' -> ['ctrl', 'shift', 'a'])
        time.sleep(random.uniform(*RANDOM_DELAY))
    except Exception as e:
        print(f"Erro ao pressionar a tecla {hotkey}: {e}")

def write_text(text):
    """
    Digita um texto.
    :param text: Texto a ser digitado.
    """
    try:
        pyautogui.write(text, interval=random.uniform(*RANDOM_DELAY))
        time.sleep(random.uniform(*RANDOM_DELAY))
    except Exception as e:
        print(f"Erro ao digitar o texto {text}: {e}")

def press_key(key):
    """
    Pressiona uma única tecla.
    :param key: Tecla a ser pressionada (ex: 'a', 'enter', 'space').
    """
    try:
        pyautogui.press(key)
        time.sleep(random.uniform(*RANDOM_DELAY))
    except Exception as e:
        print(f"Erro ao pressionar a tecla {key}: {e}")