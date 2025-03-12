import random
import time
from config.settings import RANDOM_DELAY

def random_delay():
    """
    Gera um tempo de espera aleatório dentro do intervalo definido em RANDOM_DELAY.
    :return: Nenhum.
    """
    delay = random.uniform(*RANDOM_DELAY)
    time.sleep(delay)

def random_mouse_movement():
    """
    Move o mouse para uma posição aleatória na tela.
    :return: Nenhum.
    """
    try:
        import pyautogui
        screen_width, screen_height = pyautogui.size()
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y, duration=random.uniform(*RANDOM_DELAY))
        random_delay()
    except Exception as e:
        print(f"Erro ao mover o mouse aleatoriamente: {e}")

def random_click(position=None, button='left'):
    """
    Clica em uma posição específica ou em uma posição aleatória.
    :param position: Tupla (x, y) com as coordenadas da tela (opcional).
    :param button: Botão do mouse a ser clicado ('left' ou 'right').
    :return: Nenhum.
    """
    try:
        import pyautogui
        if position:
            pyautogui.moveTo(position[0], position[1], duration=random.uniform(*RANDOM_DELAY))
        else:
            random_mouse_movement()
        pyautogui.click(button=button)
        random_delay()
    except Exception as e:
        print(f"Erro ao clicar aleatoriamente: {e}")

def random_key_press(keys):
    """
    Pressiona uma tecla aleatória de uma lista de teclas.
    :param keys: Lista de teclas a serem pressionadas (ex: ['a', 'b', 'c']).
    :return: Nenhum.
    """
    try:
        import pyautogui
        key = random.choice(keys)
        pyautogui.press(key)
        random_delay()
    except Exception as e:
        print(f"Erro ao pressionar tecla aleatória: {e}")