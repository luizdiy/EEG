# captura.py
import tkinter as tk
import serial.tools.list_ports
import threading
import datetime
import time

#meus módulos
from grafico import Grafico  # Importa a classe Linha
from conexao import Conexao
from arquivo import write

class JanelaCaptura(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cerebrino v0.0 - Captura de Dados")

        self.nome_arquivo = ""
        self.time_window = 1
        self.conexao_ativa = False
        self.buffer_conexao = []

        # Cria o frame de botões
        button_frame = tk.Frame(master=self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Cria o label do dropdown
        port_label = tk.Label(button_frame, text="Port:")
        port_label.grid(row=0, column=0, pady=5)

        # Lê a lista de portas
        port_options = [port.device for port in serial.tools.list_ports.comports()]
        self.port_variable = tk.StringVar(button_frame)

        # Define o valor inicial da variável
        self.port_variable.set("none")  # Define "none" como valor inicial

        # Cria o OptionMenu
        self.port_dropdown = tk.OptionMenu(button_frame, self.port_variable, "none", *port_options)
        self.port_dropdown.grid(row=0, column=1, pady=5)

        # Conecta o evento de clique no dropdown
        self.port_dropdown.bind("<Button-1>", lambda event: self.update_port_options())

        # Cria o gráfico
        self.grafico = Grafico(self)  # Cria uma instância de Linha e passa a janela principal como master

        # Cria os botões
        self.button_start = tk.Button(master=button_frame, text="start", command=self.button_start_click, state=tk.NORMAL)
        self.button_start.grid(row=0, column=3, pady=5)
        self.button_stop = tk.Button(master=button_frame, text="stop", command=self.button_stop_click, state=tk.DISABLED)
        self.button_stop.grid(row=0, column=4, pady=5)
        self.button_save = tk.Button(master=button_frame, text="save", command=self.button_save_click, state=tk.DISABLED)
        self.button_save.grid(row=0, column=5, pady=5)

        #cria slider
        self.slider_rate = tk.Scale(
                           master=button_frame,
                           from_=1,
                           to=5,
                           orient=tk.HORIZONTAL,
                           label="time (s)", command=self.slider_time)
        self.slider_rate.grid(row=0, column=6, pady=5)

        # Função para atualizar o gráfico continuamente
        def update_graph():
            buffer_grafico = []
            temp = []
            pointer_conexao = 0
            while self.conexao_ativa:
                temp = self.conexao.read(pointer_conexao)
                pointer_conexao = pointer_conexao + len(temp)
                buffer_grafico = buffer_grafico + temp
                if len(buffer_grafico) > 5000:
                    del buffer_grafico[:len(buffer_grafico)-5000]
                
                self.grafico.atualiza(buffer_grafico[:(self.time_window * 1000)])
                time.sleep(0.5)  # Ajuste o intervalo de atualização aqui

        # Inicia a thread para atualizar o gráfico
        self.thread_grafico = threading.Thread(target=update_graph)


    # Função para atualizar as opções do dropdown
    def update_port_options(self):
        """Atualiza as opções do dropdown com as portas disponíveis,
        mantendo "none" na primeira posição.
        """
        self.port_dropdown['menu'].delete(0, 'end')  # Limpa as opções existentes

        # Adiciona "none" como a primeira opção
        self.port_dropdown['menu'].add_command(label="none", command=lambda value="none": self.port_variable.set(value))

        # Adiciona as portas disponíveis
        new_options = [port.device for port in serial.tools.list_ports.comports()]
        for option in new_options:
            self.port_dropdown['menu'].add_command(label=option, command=lambda value=option: self.port_variable.set(value))

        # Define "none" como o valor inicial se houver novas opções
        if new_options:
            self.port_variable.set("none")

    # Funções dos botões
    def button_start_click(self):
        if not self.port_variable.get() == 'none':
            print("start\n")
            data_hora = datetime.datetime.now()
            self.nome_arquivo = "../dados/" + f"{data_hora.strftime('%y%m%d-%H-%M-%S')}.raw"
        
            selected_port = self.port_variable.get()
            self.conexao = Conexao()
            #print(f"Porta selecionada: {selected_port}")
            self.conexao.connect(selected_port, 115200)
            self.conexao.start()
            self.conexao_ativa = True
            self.thread_grafico.start()
            self.button_start.config(state=tk.DISABLED)
            self.button_stop.config(state=tk.NORMAL)
            self.button_save.config(state=tk.DISABLED)
            self.port_dropdown.config(state=tk.DISABLED)

    def button_stop_click(self):
        self.buffer_conexao = self.conexao.read()
        self.conexao.stop()
        self.conexao.join()
        self.conexao_ativa = False
        self.button_start.config(state=tk.NORMAL)
        self.button_save.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)
        self.port_dropdown.config(state=tk.NORMAL)

    def button_save_click(self):    
        write(self.nome_arquivo, self.buffer_conexao)
        self.button_start.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)
        self.button_save.config(state=tk.DISABLED)
        self.port_dropdown.config(state=tk.NORMAL)
        
    def slider_time(self, new_val):
        self.time_window = int(new_val)
        print(self.time_window)