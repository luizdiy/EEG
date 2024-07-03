#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 13:07:23 2024

@author: luiz
"""

#import numpy as np
from scipy.signal import butter, lfilter

def filtro_passa_faixa(dados, lowcut, highcut, fs):
  """
  Aplica um filtro passa-faixa Butterworth de segunda ordem.

  Args:
    dados: Lista de dados do sinal.
    lowcut: Frequência de corte inferior do filtro em Hz.
    highcut: Frequência de corte superior do filtro em Hz.
    fs: Frequência de amostragem do sinal em Hz.

  Returns:
    dados_filtrados: Lista de dados do sinal filtrado.
  """

  nyq = 0.5 * fs
  low = lowcut / nyq
  high = highcut / nyq
  b, a = butter(2, [low, high], btype='band')
  dados_filtrados = lfilter(b, a, dados)
  return dados_filtrados

def aplicar_filtros(dados):
  return [
      filtro_passa_faixa(dados, 0.5, 3, 1000),
      filtro_passa_faixa(dados, 3.9, 7, 1000),
      filtro_passa_faixa(dados, 7.9, 13, 1000),
      filtro_passa_faixa(dados, 13.9, 30, 1000)
  ]
"""
# Define as frequências de corte e a frequência de amostragem
lowcut = 0.5  # Hz
highcut = 3  # Hz
fs = 1000  # Hz

# Aplica o filtro passa-faixa
dados_filtrados = filtro_passa_faixa(dados, lowcut, highcut, fs)
"""