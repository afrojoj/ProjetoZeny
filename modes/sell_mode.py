import time
import random
from utils.image_recognition import find_image_on_screen
from utils.mouse_controller import move_and_click
from utils.keyboard_controller import press_hotkey
from config.settings import UI_ELEMENTS_DIR, WAIT_TIME, RANDOM_DELAY
from config.hotkeys import HOTKEYS

def sell_mode():
    print("Modo Venda ativado!")
    press_hotkey(HOTKEYS["use_fly_wing"])  # Teleporta para uma área segura
    time.sleep(random.uniform(*RANDOM_DELAY))

    # Abre a loja de utilidades de bolso
    press_hotkey(HOTKEYS["open_shop"])
    time.sleep(random.uniform(*RANDOM_DELAY))

    # Vende todos os itens não bloqueados
    sell_button_image = f"{UI_ELEMENTS_DIR}sell_button.png"  # Caminho da imagem do botão de venda
    sell_button_location = find_image_on_screen(sell_button_image)
    if sell_button_location:
        print("Vendendo itens...")
        move_and_click(sell_button_location)  # Clica no botão de vender
        time.sleep(random.uniform(*RANDOM_DELAY))

    # Abre a Kafra
    press_hotkey(HOTKEYS["open_kafra"])
    time.sleep(random.uniform(*RANDOM_DELAY))

    # Transfere itens predefinidos para a Kafra
    items_to_store = ["item_emperium.png", "item_erva_azul.png", "item_mastela.png"]  # Insira os nomes das imagens dos itens
    for item in items_to_store:
        item_image = f"{UI_ELEMENTS_DIR}{item}"  # Caminho da imagem do item
        item_location = find_image_on_screen(item_image)
        if item_location:
            print(f"Transferindo {item} para a Kafra...")
            move_and_click(item_location)  # Seleciona o item
            press_hotkey(HOTKEYS["transfer_items"])  # Transfere o item para a Kafra
            time.sleep(random.uniform(*RANDOM_DELAY))

    print("Venda e armazenamento concluídos! Voltando ao modo farme.")