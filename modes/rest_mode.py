import time
import random
from utils.image_recognition import find_monster_on_screen, read_text_from_image
from utils.mouse_controller import move_and_click
from utils.keyboard_controller import press_hotkey
from config.settings import UI_ELEMENTS_DIR, WAIT_TIME, RANDOM_DELAY
from config.hotkeys import HOTKEYS

def rest_mode():
    print("Modo Descanso ativado!")
    press_hotkey(HOTKEYS["use_fly_wing"])  # Teleporta para uma área segura
    time.sleep(random.uniform(*RANDOM_DELAY))

    while True:
        # Verifica se o SP já regenerou o suficiente
        sp_image = f"{UI_ELEMENTS_DIR}sp_bar.png"  # Caminho da imagem da barra de SP
        sp_text = read_text_from_image(sp_image)
        if sp_text and int(sp_text) >= 50:  # Volta ao modo farme se o SP estiver acima de 50%
            print("SP regenerado! Voltando ao modo farme.")
            return

        # Ataca monstros próximos com ataques básicos
        monsters = ["agressor", "aquecedor", "congelador", "batedor"]
        monster_found = False
        for monster_name in monsters:
            monster_location = find_monster_on_screen(monster_name)
            if monster_location:
                print(f"Monstro próximo encontrado! Atacando...")
                move_and_click(monster_location)  # Ataque básico (clique do mouse)
                time.sleep(random.uniform(*RANDOM_DELAY))
                monster_found = True
                break  # Sai do loop (monstros)

        if not monster_found:
            print("Nenhum monstro próximo encontrado. Aguardando regeneração de SP...")
            time.sleep(WAIT_TIME)