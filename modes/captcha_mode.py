import time
import random
import pyautogui
from utils.image_recognition import find_image_on_screen
from utils.ocr import read_text_from_image
from utils.keyboard_controller import press_hotkey
from config.settings import CAPTCHA_DIR, WAIT_TIME, RANDOM_DELAY
from config.hotkeys import HOTKEYS

def captcha_mode():
    print("Modo Captcha ativado!")
    press_hotkey(HOTKEYS["toggle_4tools"])  # Desliga o 4tools
    time.sleep(random.uniform(*RANDOM_DELAY))

    # Resolve o captcha de caracteres
    captcha_image = os.path.join(CAPTCHA_DIR, "captcha_popup.png")  # Insira o caminho da imagem
    captcha_text = read_text_from_image(captcha_image)
    if captcha_text:
        pyautogui.write(captcha_text)  # Digita o texto do captcha
        time.sleep(random.uniform(*RANDOM_DELAY))
        pyautogui.press("enter")  # Confirma o captcha


    # Resolve o captcha da sala secreta
    npc_image = os.path.join(CAPTCHA_DIR, "npc.png")  # Insira o caminho da imagem
    npc_location = find_image_on_screen(npc_image)
    if npc_location:
        move_and_click(npc_location)  # Clica no NPC
        time.sleep(random.uniform(*RANDOM_DELAY))

        # Identifica os números em vermelho
        numbers_image = os.path.join(CAPTCHA_DIR, "numbers.png")  # Insira o caminho da imagem
        numbers_text = read_text_from_image(numbers_image)
        if numbers_text:
            pyautogui.write(numbers_text)  # Digita os números
            time.sleep(random.uniform(*RANDOM_DELAY))
            pyautogui.press("enter")  # Confirma os números

    # Volta ao modo farme
    time.sleep(random.uniform(3, 5))  # Espera um tempo aleatório
    press_hotkey(HOTKEYS["toggle_4tools"])  # Liga o 4tools novamente
    print("Captcha resolvido! Voltando ao modo farme.")