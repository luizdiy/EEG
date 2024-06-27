import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Linha:
    def __init__(self, master):
        self.master = master  # Armazena a referência ao master (janela Tkinter)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        #self.ax.set_title("Gráfico Dinâmico")
        #self.ax.set_xlabel("Índice")
        #self.ax.set_ylabel("Valor")
        self.data = []

        # Configura os limites do eixo y aqui
        self.ax.set_ylim(0, 1023)

        # Cria o canvas TkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def atualiza(self, lista):

        self.data = lista
        self.ax.clear()
        
        self.ax.plot(self.data, color='b')
        self.canvas.draw()         

    def fecha(self):
        # Fecha a janela do gráfico
        self.master.destroy()
        
    def on_close(self, event):
        print("O botão Fechar foi clicado!")
        self.fecha()  # Chama o método fecha para fechar a janela
        
    def ativo(self):
        # Verifica se a janela do gráfico ainda está aberta
        return self.master.winfo_exists()