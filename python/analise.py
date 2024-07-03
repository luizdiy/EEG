#!/bin/python3
import tkinter as tk
from tkinter import filedialog
import os
import arquivo
import filtro
from grafico import GraficoMultiplo  # Importe a classe GraficoMultiplo do módulo grafico

root = tk.Tk()
root.title("Cerebrino v0.0")

# Cria uma instância da classe GraficoMultiplo
gfm = GraficoMultiplo(root)
button_frame = tk.Frame(master=root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

def selecionar_arquivo():
    """Abre uma caixa de diálogo para o usuário selecionar um arquivo."""
    global arquivo_selecionado
    arquivo_selecionado = filedialog.askopenfilename(
        initialdir="../dados",
        title="Selecione um arquivo",
        filetypes=(("Arquivos de texto", "*.raw"), ("Todos os arquivos", "*.*"))
    )
    if arquivo_selecionado:
        nome_arquivo = os.path.basename(arquivo_selecionado)
        label_arquivo["text"] = f"Arquivo: {nome_arquivo}"
        dados = arquivo.read(arquivo_selecionado)  # Lê os dados do arquivo
        dados = filtro.aplicar_filtros(dados)  # Aplica os filtros
        gfm.plot(dados)  # Plota os dados usando o método plot() da classe GraficoMultiplo

# Cria os botões e o rótulo
botao_selecionar = tk.Button(master=button_frame, text="Selecionar Arquivo", command=selecionar_arquivo)
botao_selecionar.grid(row=0, column=0, pady=5)

label_arquivo = tk.Label(master=button_frame, text="")
label_arquivo.grid(row=0, column=2, pady=5)

root.mainloop()
