import threading
import os
import time
import random
from core.state_machine import StateMachine
from utils.image_recognition import find_image_on_screen
from utils.ocr import read_text_from_image
from config.settings import UI_ELEMENTS_DIR, WAIT_TIME, RANDOM_DELAY
from config.hotkeys import HOTKEYS


class Bot:
    def __init__(self):
        self.state_machine = StateMachine()
        self.state_machine.set_state("farm")  # Começa no modo farme
        self.sp_threshold = 35  # Limite de SP para entrar em descanso
        self.inventory_threshold = 90  # Limite de slots no inventário para entrar em venda
        self.max_sp = 704  # SP máximo (ajuste conforme necessário)
        self.screenshot_cache = None  # Cache para capturas de tela
        self.running = True  # Controle para encerrar threads

        # Criação das threads
        self.screenshot_thread = threading.Thread(target=self.update_screenshot_cache)
        self.condition_thread = threading.Thread(target=self.check_conditions_thread)

    def start(self):
        """
        Inicia o bot e gerencia as transições entre os estados.
        """
        print("Bot iniciado!")

        # Inicia as threads em segundo plano
        self.screenshot_thread.start()
        self.condition_thread.start()

        try:
            while self.running:
                self.state_machine.run()  # Executa o estado atual
                time.sleep(WAIT_TIME)  # Espera um pouco antes da próxima iteração
        except KeyboardInterrupt:
            print("Bot interrompido manualmente! Encerrando...")
            self.stop()

        # Aguarda o fim das threads
        self.screenshot_thread.join()
        self.condition_thread.join()

    def stop(self):
        """
        Para o bot e finaliza as threads.
        """
        self.running = False
        print("Finalizando o bot...")

    def update_screenshot_cache(self):
        """
        Atualiza o cache de captura de tela continuamente em uma thread separada.
        """
        while self.running:
            try:
                import pyautogui
                self.screenshot_cache = pyautogui.screenshot()
                time.sleep(0.2)  # Evita capturas muito frequentes
            except Exception as e:
                print(f"Erro ao capturar a tela: {e}")

    def check_conditions_thread(self):
        """
        Verifica condições em um loop contínuo em uma thread separada.
        """
        while self.running:
            self.check_conditions()
            time.sleep(1)  # Intervalo de verificação

    def check_conditions(self):
        """
        Verifica as condições do jogo e altera o estado do bot conforme necessário.
        """
        current_state = self.state_machine.current_state

        # Verifica se o inventário está cheio
        if self.is_inventory_full() and current_state != "sell":
            print("Inventário cheio! Entrando no modo venda.")
            self.state_machine.set_state("sell")
            return

        # Verifica se o SP está baixo
        if self.is_sp_low() and current_state != "rest":
            print("SP baixo! Entrando no modo descanso.")
            self.state_machine.set_state("rest")
            return

        # Verifica se há captcha
        if self.is_captcha_present() and current_state != "captcha":
            print("Captcha detectado! Entrando no modo captcha.")
            self.state_machine.set_state("captcha")
            return

        # Se não houver condições especiais, volta para o modo farme
        if current_state != "farm" and not self.is_sp_low() and not self.is_inventory_full() and not self.is_captcha_present():
            print("Condições normais. Entrando no modo farme.")
            self.state_machine.set_state("farm")

    def is_inventory_full(self):
        """
        Verifica se o inventário está cheio.
        :return: True se o inventário estiver cheio, False caso contrário.
        """
        # Exemplo: Verifica a quantidade de slots usados no inventário
        inventory_image = os.path.join(UI_ELEMENTS_DIR, "inventory_slots.png")  # Insira o caminho da imagem
        inventory_text = read_text_from_image(inventory_image)
        if inventory_text:
            used_slots = int(inventory_text.split("/")[0])  # Assume que o texto está no formato "X/100"
            return used_slots >= self.inventory_threshold
        return False

    def is_sp_low(self):
        """
        Verifica se o SP está abaixo do limite.
        :return: True se o SP estiver baixo, False caso contrário.
        """
        # Exemplo: Verifica a barra de SP
        sp_image = os.path.join(UI_ELEMENTS_DIR, "sp_bar.png")  # Insira o caminho da imagem
        sp_text = read_text_from_image(sp_image)
        if sp_text:
            current_sp = int(sp_text)  # Assume que o texto é o valor atual de SP
            return current_sp < self.sp_threshold
        return False

    def is_captcha_present(self):
        """
        Verifica se há um captcha na tela.
        :return: True se um captcha for detectado, False caso contrário.
        """
        # Exemplo: Verifica a presença de um captcha
        captcha_image = os.path.join(UI_ELEMENTS_DIR, "captcha_popup.png")  # Insira o caminho da imagem
        return find_image_on_screen(captcha_image) is not None