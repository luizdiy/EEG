# analise.py
import tkinter as tk
from tkinter import filedialog
import os

from arquivo import read  # Importar módulo arquivo
from filtro import aplicar_filtros  # Importar módulo filtro
from grafico import GraficoMultiplo  # Importar módulo grafico

class JanelaAnalise(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cerebrino v0.0 - Análise de Dados")

        # Cria o frame de botões
        button_frame = tk.Frame(master=self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Cria o botão para selecionar arquivo
        botao_selecionar = tk.Button(master=button_frame, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        botao_selecionar.grid(row=0, column=0, pady=5)

        # Cria o label para mostrar o nome do arquivo
        self.label_arquivo = tk.Label(master=button_frame, text="")
        self.label_arquivo.grid(row=0, column=2, pady=5)

        # Cria o gráfico
        self.gfm = GraficoMultiplo(self)  # Cria uma instância de GraficoMultiplo

    def selecionar_arquivo(self):
        """Abre uma caixa de diálogo para o usuário selecionar um arquivo."""
        global arquivo_selecionado
        arquivo_selecionado = filedialog.askopenfilename(
            initialdir="./dados",
            title="Selecione um arquivo",
            filetypes=(("Arquivos de texto", "*.raw"), ("Todos os arquivos", "*.*"))
        )
        if arquivo_selecionado:
            nome_arquivo = os.path.basename(arquivo_selecionado)
            self.label_arquivo["text"] = f"Arquivo: {nome_arquivo}"
            dados = read(arquivo_selecionado)  # Lê os dados do arquivo
            dados = aplicar_filtros(dados)  # Aplica os filtros
            self.gfm.plot(dados)  # Plota os dados usando o método plot() da classe GraficoMultiplo
