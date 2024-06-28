#!/bin/python3
import tkinter as tk
import serial.tools.list_ports
import threading
import datetime
import time

#meus módulos
from grafico import Linha  # Importa a classe Linha
from conexao import Conexao
from arquivo import write


nome_arquivo = ""
taxa = 1
conexao_ativa = False
dados = []

# Cria a janela principal
root = tk.Tk()
root.title("Cerebrino")

# Cria o frame de botões
button_frame = tk.Frame(master=root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Cria o label do dropdown
port_label = tk.Label(button_frame, text="Port:")
port_label.grid(row=0, column=0, pady=5)

# Lê a lista de portas
port_options = [port.device for port in serial.tools.list_ports.comports()]
port_variable = tk.StringVar(button_frame)

# Define o valor inicial da variável
port_variable.set("none")  # Define "none" como valor inicial

# Cria o OptionMenu
port_dropdown = tk.OptionMenu(button_frame, port_variable, "none", *port_options)
port_dropdown.grid(row=0, column=1, pady=5)

# Conecta o evento de clique no dropdown
port_dropdown.bind("<Button-1>", lambda event: update_port_options())

# Cria o gráfico
grafico = Linha(root)  # Cria uma instância de Linha e passa a janela principal como master

# Cria os botões
button_start = tk.Button(master=button_frame, text="start")
button_start.grid(row=0, column=3, pady=5)
button_stop = tk.Button(master=button_frame, text="stop")
button_stop.grid(row=0, column=4, pady=5)
button_save = tk.Button(master=button_frame, text="save")
button_save.grid(row=0, column=5, pady=5)

# Função para atualizar o gráfico continuamente
def update_graph():
    while conexao_ativa:
        dados = conexao.read(int(1000 * taxa))
        grafico.atualiza(dados)
        time.sleep(taxa)  # Ajuste o intervalo de atualização aqui


# Função para atualizar as opções do dropdown
def update_port_options():
    """Atualiza as opções do dropdown com as portas disponíveis,
    mantendo "none" na primeira posição.
    """
    port_dropdown['menu'].delete(0, 'end')  # Limpa as opções existentes

    # Adiciona "none" como a primeira opção
    port_dropdown['menu'].add_command(label="none", command=lambda value="none": port_variable.set(value))

    # Adiciona as portas disponíveis
    new_options = [port.device for port in serial.tools.list_ports.comports()]
    for option in new_options:
        port_dropdown['menu'].add_command(label=option, command=lambda value=option: port_variable.set(value))

    # Define "none" como o valor inicial se houver novas opções
    if new_options:
        port_variable.set("none")

# Funções dos botões
def button_start_click():
    if not port_variable.get() == 'none':
        print("start\n")
        global nome_arquivo
        data_hora = datetime.datetime.now()
        nome_arquivo = "../dados/" + f"{data_hora.strftime('%y%m%d-%H-%M-%S')}.raw"
    
        selected_port = port_variable.get()
        global conexao
        conexao = Conexao()
        #print(f"Porta selecionada: {selected_port}")
        conexao.connect(selected_port, 115200)
        conexao.start()
        global conexao_ativa
        conexao_ativa = True
        threading.Thread(target=update_graph).start()
        button_start.config(state=tk.DISABLED)
        button_stop.config(state=tk.NORMAL)
        button_save.config(state=tk.DISABLED)
        port_dropdown.config(state=tk.DISABLED)
    
def button_stop_click():
    global dados
    dados = conexao.read()
    conexao.stop()
    conexao.join()
    global conexao_ativa
    conexao_ativa = False
    button_start.config(state=tk.NORMAL)
    button_save.config(state=tk.NORMAL)
    button_stop.config(state=tk.DISABLED)
    port_dropdown.config(state=tk.NORMAL)

def button_save_click():    
    write(nome_arquivo, dados)
    button_start.config(state=tk.NORMAL)
    button_stop.config(state=tk.DISABLED)
    button_save.config(state=tk.DISABLED)
    port_dropdown.config(state=tk.NORMAL)
    
    
def update_frequency(new_val):
    # retrieve frequency
    global taxa
    taxa = 1 / float(new_val)



slider_update = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL,
                              command=update_frequency, label="Frequency [Hz]")

    
# Conecta as funções nos botões
slider_update.pack(side=tk.BOTTOM)
button_start.config(command=button_start_click,state=tk.NORMAL)
button_stop.config(command=button_stop_click,state=tk.DISABLED)
button_save.config(command=button_save_click,state=tk.DISABLED)


# Inicia o loop principal do Tkinter
root.mainloop()
