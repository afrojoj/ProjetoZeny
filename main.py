import os
import sys
from core.bot import Bot

if __name__ == "__main__":
    # Verifica se o processo TalesDog.exe está rodando
    if os.system("tasklist | findstr TalesDog.exe") == 0:
        print("Feche o TalesDog.exe antes de rodar o bot.")
        sys.exit()

    # Inicia o bot
    bot = Bot()
    bot.start()