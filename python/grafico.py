import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import matplotlib.animation as animation
import sys #captura tecla fechar janela
#1from IPython.display import display, clear_output
    
class Dinamico:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Gráfico Dinâmico")
        self.ax.set_xlabel("Índice")
        self.ax.set_ylabel("Valor")
        self.data = []
        #self.ativa = True

    def cria(self):
        """Cria uma janela para o gráfico usando o módulo matplotlib."""
        plt.ion()  # Ativa o modo interativo para atualização contínua do gráfico
        plt.show()

    def atualiza(self, lista):    
        """
            Recebe uma lista com 1000 inteiros e atualiza a janela do gráfico com os inteiros da lista.
            A cada chamada de atualiza(lista), a instância da janela será atualizada com o gráfico dos novos dados.
        """
    
        self.data = lista  # Substitui os dados existentes pela nova lista
        self.ax.clear()  # Limpa o gráfico
        
        plt.ylim(0, 1023) # Configura os limites do eixo y para 0 e 1023
        #plt.xlim(0, 1)
        #plt.autoscale(False)
        
        self.ax.plot(self.data, color='b')  # Plota os dados
        plt.draw()  # Redesenha o gráfico
        plt.pause(0.1)

        # Gera e exibe o espectrograma
        #self.gspectrum(self.data)

    def gspectrum(self, dados, sr=1000, freqmax=50, window="hamming", noverlap=128, nfft=256, escala_dB=80):
        """
        Função que calcula e plota o espectrograma.

        Args:
            dados: Vetor com dados uint16.
            sr: Sample rate em Hz.
            freqmax: Frequência máxima a ser exibida no espectrograma.
            window: Tipo de janela espectral.
            noverlap: Sobreposição das janelas.
            nfft: Tamanho da FFT.
            escala_dB: Limite superior da escala em dB.

        Returns:
            None.
        """

        # Cálculo do espectrograma
        dados = np.array(dados)
        frequencias, tempos, espectrograma = spectrogram(dados, fs=sr, nfft=nfft, noverlap=noverlap, window=window)

        # Seleção das frequências abaixo da frequência máxima
        indices_frequencias = np.where(frequencias < freqmax)[0]
        frequencias = frequencias[indices_frequencias]
        espectrograma = espectrograma[indices_frequencias, :]

        # Conversão do espectrograma para dB
        espectrograma_dB = 10 * np.log10(espectrograma)

        # Plot do espectrograma (figura separada)
        fig_spec, ax_spec = plt.subplots(figsize=(8, 6))
        ax_spec.pcolormesh(tempos, frequencias, espectrograma_dB, cmap="viridis", vmin=0, vmax=escala_dB)
        ax_spec.set_xlabel("Tempo (s)")
        ax_spec.set_ylabel("Frequência (Hz)")
        ax_spec.set_title("Espectrograma")
        fig_spec.tight_layout()
        plt.show(block=Falee)  # Exibe o espectrograma em uma janela separada
          
    def fecha(self):
        plt.ioff()
        plt.close()
        
    def on_close(self, event):
        print("O botão Fechar foi clicado!")
        #self.ativa = False
        plt.close()
        
    def ativo(self):
        if plt.get_fignums():  # Retorna uma lista vazia se a janela foi fechada
            return True
        else:
            return False
        
    

# Exemplo de uso:
if __name__ == "__main__":
    dinamico = Dinamico()
    dinamico.cria()

    try:
        while True:
            # Simulando atualizações com uma lista de inteiros aleatórios
            lista_atualizacao = np.random.randint(0, 100, size=1000)
            dinamico.atualiza(lista_atualizacao)
            plt.pause(0.01)  # Pausa para atualização contínua

    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
        plt.ioff()
        plt.close()
