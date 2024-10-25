import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

class signalMeu:
    def __init__(self):
        pass

    def calcFFT(self, sinal, fs):
        N = len(sinal)
        W = np.hamming(N)  # Usando a função hamming do NumPy
        T = 1 / fs
        xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
        yf = fft(sinal * W)
        return (xf, np.abs(yf[0:N // 2]))

    def plotFFT(self, sinal, fs):
        xf, yf = self.calcFFT(sinal, fs)
        plt.figure(figsize=(10, 4))
        plt.plot(xf, yf)
        plt.title('Transformada de Fourier')
        plt.xlabel('Frequência [Hz]')
        plt.ylabel('Magnitude')
        plt.grid()
        plt.show()
