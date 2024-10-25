# Importar todas as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from scipy.signal import find_peaks


def main():
    # Instanciar a classe do sinal
    signal = signalMeu()

    # Parâmetros do sounddevice
    fs = 44100  # Frequência de amostragem
    sd.default.samplerate = fs
    sd.default.channels = 1  # Gravação mono
    duracao = 2  # Duração da gravação em segundos
    numAmostras = int(duracao * fs)

    print("A captura de áudio começará em 3 segundos...")
    time.sleep(3)
    print("Gravando...")
    audio = sd.rec(numAmostras, samplerate=fs, channels=1)
    sd.wait()
    print("Gravação finalizada.")

    # Extrair os dados gravados
    dados = audio.flatten()  # Achatar o array se necessário

    # Criar o array de tempo
    t = np.linspace(0, duracao, numAmostras, endpoint=False)

    # Plotar o sinal no domínio do tempo
    plt.figure(figsize=(10, 4))
    plt.plot(t, dados)
    plt.title("Sinal no Domínio do Tempo")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    # Calcular a transformada de Fourier
    xf, yf = signal.calcFFT(dados, fs)

    # Plotar o sinal no domínio da frequência
    plt.figure(figsize=(10, 4))
    plt.plot(xf, yf)
    plt.title("Transformada de Fourier")
    plt.xlabel("Frequência [Hz]")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()

    # Identificar os picos no domínio da frequência
    # Ajustar os parâmetros de altura e distância conforme necessário
    picos, propriedades = find_peaks(yf, height=0.1 * np.max(yf), distance=20)
    freq_picos = xf[picos]
    magnitudes_picos = yf[picos]

    print("Frequências de pico detectadas:")
    for freq in freq_picos:
        print(f"{freq:.2f} Hz")

    # Mapeamento das frequências DTMF (mesmo que antes)
    dtmf_frequencias = {
        '1': (697, 1209),
        '2': (697, 1336),
        '3': (697, 1477),
        '4': (770, 1209),
        '5': (770, 1336),
        '6': (770, 1477),
        '7': (852, 1209),
        '8': (852, 1336),
        '9': (852, 1477),
        '0': (941, 1336),
    }

    # Encontrar as duas frequências mais próximas das frequências DTMF
    possiveis_teclas = []
    for tecla, (freq_baixa, freq_alta) in dtmf_frequencias.items():
        # Verificar se as frequências detectadas estão próximas das frequências DTMF
        for freq_detectada in freq_picos:
            if abs(freq_detectada - freq_baixa) < 10:
                for freq_detectada2 in freq_picos:
                    if abs(freq_detectada2 - freq_alta) < 10:
                        possiveis_teclas.append(tecla)

    # Remover duplicatas
    possiveis_teclas = list(set(possiveis_teclas))

    if len(possiveis_teclas) == 1:
        print(f"A tecla detectada é: {possiveis_teclas[0]}")
    elif len(possiveis_teclas) > 1:
        print("Múltiplas teclas possíveis detectadas:", possiveis_teclas)
    else:
        print("Nenhuma tecla DTMF válida detectada.")

if __name__ == "__main__":
    main()
