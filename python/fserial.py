#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import threading

class LeSerial(threading.Thread):
    def __init__(self, porta_serial, baud_rate):
        super().__init__()
        self.porta_serial = porta_serial
        self.baud_rate = baud_rate
        self.dados = []
        self._rodando = True

        # Inicializa a porta serial
        try:
            self.ser = serial.Serial(self.porta_serial, self.baud_rate)
        except serial.SerialException as e:
            print(f"Erro ao abrir a porta serial: {e}")
            self._rodando = False


    def run(self):
        while self._rodando:
            # Lê um byte da porta serial
            byte_lido = ord(self.ser.read(1))

            # Se o byte for um byte alto válido, lê o byte baixo e monta o valor inteiro
            if (byte_lido & 0b10000000) == 0b10000000:
                byte_baixo = ord(self.ser.read(1))
                valor_inteiro = (byte_baixo & 0b1111111) | ((byte_lido & 0b111) << 7)
                self.dados.append(valor_inteiro)
            

    def parar(self):
        self._rodando = False
        self.ser.close()
        
    def ledados(self, nbytes):
        """
        Retorna os últimos "nbytes" de dados da lista "dados".
    
        Argumentos:
            nbytes: O número de bytes a serem retornados.
    
        Retorna:
            Uma lista com os últimos "nbytes" de dados da lista "dados".
        """
    
        # Se o número de bytes a serem retornados for maior que o tamanho da lista, retorna a lista toda
        if nbytes > len(self.dados):
            return self.dados
    
        # Retorna os últimos "nbytes" de dados da lista
        return self.dados[-nbytes:]

    def letudo(self):
        #print("letudo")
        return self.dados