import time
import random
from utils.image_recognition import find_monster_on_screen
from utils.mouse_controller import move_and_click
from utils.keyboard_controller import press_hotkey
from config.settings import WAIT_TIME, RANDOM_DELAY
from config.hotkeys import HOTKEYS

def farm_mode():
    print("Modo Farme ativado!")
    while True:
        # Lista de monstros para procurar
        monsters = ["agressor", "aquecedor", "congelador", "batedor"]

        # Procura por qualquer monstro na tela
        monster_found = False
        for monster_name in monsters:
            monster_location = find_monster_on_screen(monster_name)
            if monster_location:
                print(f"{monster_name.capitalize()} encontrado! Atacando...")
                move_and_click(monster_location)  # Move o mouse e clica no monstro
                press_hotkey(HOTKEYS["use_skill"])  # Usa a habilidade
                time.sleep(random.uniform(*RANDOM_DELAY))  # Aleatorização de tempo

                # Teleporta para outro local no mapa
                press_hotkey(HOTKEYS["use_fly_wing"])
                time.sleep(random.uniform(*RANDOM_DELAY))

                monster_found = True
                break  # Sai do loop (monstros)

        if not monster_found:
            print("Nenhum monstro encontrado. Procurando novamente...")
            time.sleep(WAIT_TIME)