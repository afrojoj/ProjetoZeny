import os
import sys
import signal
import traceback
from core.bot import Bot


def signal_handler(sig, frame):
    """
    Manipulador de sinais para capturar Ctrl+C e outras interrupções
    """
    print("\nSinal de interrupção recebido. Finalizando o bot...")
    if 'bot' in globals() and bot is not None:
        bot.stop()
    sys.exit(0)


if __name__ == "__main__":
    # Registra manipuladores de sinais
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill command

    try:
        # Verifica se o processo TalesDog.exe está rodando
        if os.system("tasklist | findstr TalesDog.exe") == 0:
            print("Feche o TalesDog.exe antes de rodar o bot.")
            sys.exit(1)

        # Inicia o bot
        print("Iniciando o bot...")
        bot = Bot()
        bot.start()

    except Exception as e:
        print(f"\nErro inesperado: {str(e)}")
        print("Detalhes do erro:")
        traceback.print_exc()

        # Garante que o bot seja encerrado corretamente mesmo em caso de erro
        if 'bot' in globals() and bot is not None:
            bot.stop()

        sys.exit(1)