import time
import random
import pyautogui
from config.settings import RANDOM_DELAY

def move_and_click(position, button='left'):
    """
    Move o mouse para uma posição e clica.
    :param position: Tupla (x, y) com as coordenadas da tela.
    :param button: Botão do mouse a ser clicado ('left' ou 'right').
    """
    try:
        # Move o mouse para a posição com um movimento suave
        pyautogui.moveTo(position[0], position[1], duration=random.uniform(*RANDOM_DELAY))
        time.sleep(random.uniform(*RANDOM_DELAY))

        # Clica com o botão especificado
        pyautogui.click(button=button)
        time.sleep(random.uniform(*RANDOM_DELAY))
    except Exception as e:
        print(f"Erro ao mover e clicar o mouse: {e}")

def drag_and_drop(start_position, end_position, button='left'):
    """
    Arrasta o mouse de uma posição para outra.
    :param start_position: Tupla (x, y) com as coordenadas iniciais.
    :param end_position: Tupla (x, y) com as coordenadas finais.
    :param button: Botão do mouse a ser pressionado ('left' ou 'right').
    """
    try:
        # Move o mouse para a posição inicial
        pyautogui.moveTo(start_position[0], start_position[1], duration=random.uniform(*RANDOM_DELAY))
        time.sleep(random.uniform(*RANDOM_DELAY))

        # Arrasta o mouse para a posição final
        pyautogui.dragTo(end_position[0], end_position[1], button=button, duration=random.uniform(*RANDOM_DELAY))
        time.sleep(random.uniform(*RANDOM_DELAY))
    except Exception as e:
        print(f"Erro ao arrastar e soltar o mouse: {e}")

def random_move():
    """
    Move o mouse para uma posição aleatória na tela.
    """
    try:
        screen_width, screen_height = pyautogui.size()
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y, duration=random.uniform(*RANDOM_DELAY))
        time.sleep(random.uniform(*RANDOM_DELAY))
    except Exception as e:
        print(f"Erro ao mover o mouse aleatoriamente: {e}")