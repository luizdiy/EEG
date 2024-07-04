#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 19:48:08 2024

@author: luiz
"""

import tkinter as tk
from captura import JanelaCaptura
from analise import JanelaAnalise

class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cerebrino v0.0")

        # Cria os botões
        botao_captura = tk.Button(self, text="Captura", command=self.abrir_janela_captura)
        botao_captura.pack(pady=10)

        botao_analise = tk.Button(self, text="Análise", command=self.abrir_janela_analise)
        botao_analise.pack(pady=10)

    def abrir_janela_captura(self):
        JanelaCaptura(self)

    def abrir_janela_analise(self):
        JanelaAnalise(self)

# Iniciar a aplicação
if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()