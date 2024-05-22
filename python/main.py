#!/usr/bin/python3
# -*- coding: utf-8 -*-
#from arquivo import learquivo, gravaarquivo #(path, inicio, nbytes)
#from grafico import gespectro, gsinal, dinamico
from fserial import LeSerial
#from lista import ListaCircular
from grafico import Dinamico
from arquivo import gravaarquivo
import datetime
import time

# Inicialização da serial
porta_serial = '/dev/rfcomm0'
#porta_serial = '/dev/ttyACM0'
baud_rate = 115200
data_hora = datetime.datetime.now()
nome_arquivo = "../dados/" + f"{data_hora.strftime('%y%m%d-%H-%M-%S')}.eeg"
Fs = 10000

def encerra():
    print("encerra grafico")
    grafico.fecha()
    print("grava arquivo")
    gravaarquivo(nome_arquivo, le_serial.letudo())
    print("para serial ")
    le_serial.parar()
    print("fim encerra")

# Crie uma instância da classe
try:
    le_serial = LeSerial(porta_serial, baud_rate)

except KeyboardInterrupt:
    print("\nPorta serial não encontrada")
    encerra()

le_serial.start()
grafico = Dinamico()
grafico.cria()

try:
    inicio = time.time()
    while grafico.ativo():
    #while time.time() - inicio < 180:
        dados_lidos = le_serial.ledados(1000)
        grafico.atualiza(dados_lidos)
        time.sleep(0.1)
        #print("*")
    encerra()
except KeyboardInterrupt:
     print("\nEncerrado pelo teclado.")
     encerra()
