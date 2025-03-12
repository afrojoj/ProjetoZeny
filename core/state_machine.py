from modes.farm_mode import farm_mode
from modes.rest_mode import rest_mode
from modes.sell_mode import sell_mode
from modes.captcha_mode import captcha_mode

class StateMachine:
    def __init__(self):
        self.current_state = None
        self.states = {
            "farm": farm_mode,
            "rest": rest_mode,
            "sell": sell_mode,
            "captcha": captcha_mode,
        }

    def set_state(self, new_state):
        """
        Altera o estado atual do bot.
        :param new_state: Nome do novo estado (farm, rest, sell, captcha).
        """
        if new_state in self.states:
            self.current_state = new_state
            print(f"Estado alterado para: {new_state}")
        else:
            print(f"Estado inválido: {new_state}")

    def run(self):
        """
        Executa o estado atual do bot.
        """
        if self.current_state:
            print(f"Executando estado: {self.current_state}")
            self.states[self.current_state]()
        else:
            print("Nenhum estado definido.")