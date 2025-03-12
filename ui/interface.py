import tkinter as tk
from tkinter import messagebox
from config.hotkeys import HOTKEYS

class BotInterface:
    def __init__(self, root):
        """
        Inicializa a interface do bot.
        :param root: Janela principal do Tkinter.
        """
        self.root = root
        self.root.title("Configuração do Bot")
        self.root.geometry("400x300")

        # Dicionário para armazenar os atalhos configurados
        self.hotkeys = HOTKEYS.copy()

        # Cria os widgets da interface
        self.create_widgets()

    def create_widgets(self):
        """
        Cria os widgets da interface.
        """
        # Título
        title_label = tk.Label(self.root, text="Configuração de Atalhos", font=("Arial", 16))
        title_label.pack(pady=10)

        # Frame para os campos de entrada
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Campos de entrada para cada atalho
        self.entries = {}
        for i, (hotkey_name, hotkey_value) in enumerate(HOTKEYS.items()):
            label = tk.Label(input_frame, text=f"{hotkey_name.capitalize()}:")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            entry = tk.Entry(input_frame)
            entry.insert(0, hotkey_value)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[hotkey_name] = entry

        # Botão de salvar
        save_button = tk.Button(self.root, text="Salvar", command=self.save_hotkeys)
        save_button.pack(pady=20)

    def save_hotkeys(self):
        """
        Salva os atalhos configurados.
        """
        try:
            for hotkey_name, entry in self.entries.items():
                new_value = entry.get().strip()
                if new_value:
                    self.hotkeys[hotkey_name] = new_value

            # Exibe uma mensagem de sucesso
            messagebox.showinfo("Sucesso", "Atalhos salvos com sucesso!")
            print("Atalhos atualizados:", self.hotkeys)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar os atalhos: {e}")

def run_interface():
    """
    Executa a interface do bot.
    """
    root = tk.Tk()
    app = BotInterface(root)
    root.mainloop()