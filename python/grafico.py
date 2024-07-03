import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

class Grafico:
    def __init__(self, master):
        self.master = master  # Armazena a referência ao master (janela Tkinter)
        self.fig = Figure(figsize=(15, 8), dpi=100)
        self.ax = self.fig.add_subplot()
        #self.ax.set_title("Gráfico Dinâmico")
        #self.ax.set_xlabel("Índice")
        #self.ax.set_ylabel("Valor")
        self.buffer = []
        self.read_pointer = 0

        # Configura os limites do eixo y aqui
        self.ax.set_ylim(0, 1023)

        # Cria o canvas TkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def atualiza(self, lista):

        self.buffer = lista
        self.ax.clear()
        
        self.ax.plot(self.buffer, color='b')
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
    

class GraficoMultiplo:
    def __init__(self, master):
        self.master = master  # Armazena a referência ao master (janela Tkinter)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        #self.ax.set_title("Gráfico Dinâmico")
        #self.ax.set_xlabel("Índice")
        #self.ax.set_ylabel("Valor")
        self.buffer = []
        self.read_pointer = 0

        # Configura os limites do eixo y aqui
        #self.ax.set_ylim(0, 1023)

        # Cria o canvas TkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Cria o menu do gráfico
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot(self, dados):
        """
        Lê dados do arquivo, aplica filtros e plota os resultados.
        """

        # Plota os sinais filtrados
        self.ax.clear()  # Limpa o gráfico anterior
        #self.ax.set_title("Sinais Filtrados")
        self.ax.set_xlabel("Tempo (s)")
        #self.ax.set_ylabel("Amplitude")

        # Plota cada sinal com um deslocamento vertical
        labels = ["Delta", "Teta" , "Alfa", "Beta"]  # Lista de labels
        for i, sinal in enumerate(dados):
            self.ax.plot(sinal + 800 -i * 200, label=labels[i])  # Plota no mesmo subplot

        # Configura os ticks do eixo x para o último subplot
        self.ax.set_xticks(range(0, len(dados[0]), 1000))
        self.ax.set_xticklabels([str(i / 1000) for i in range(0, len(dados[0]), 1000)])
        #self.ax.set_yticks([])  # Remove os ticks do eixo y do último subplot

        # Coloca a legenda do lado esquerdo do gráfico
        self.ax.legend(loc='center left', bbox_to_anchor=(0.05, 0.5))  # Altera a posição da legenda

        self.canvas.draw()