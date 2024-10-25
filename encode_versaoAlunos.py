# Importar as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# Mapeamento das frequências DTMF
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

def main():
    # Inicializar a classe do sinal
    signal = signalMeu()

    print("Inicializando o encoder")
    print("Aguardando entrada do usuário")

    # Pedir ao usuário um dígito entre 0 e 9
    while True:
        digito = input("Digite um número entre 0 e 9: ")
        if digito in dtmf_frequencias:
            break
        else:
            print("Entrada inválida. Por favor, digite um dígito entre 0 e 9.")

    # Obter as frequências correspondentes
    freq1, freq2 = dtmf_frequencias[digito]
    print("Gerando tons base")
    print(f"Gerando tom referente ao símbolo: {digito}")
    print(f"Frequências: {freq1}Hz e {freq2}Hz")

    # Gerar o array de tempo
    fs = 44100  # Frequência de amostragem
    duracao = 2  # Duração em segundos
    t = np.linspace(0, duracao, int(fs * duracao), endpoint=False)

    # Gerar as ondas senoidais
    tom1 = np.sin(2 * np.pi * freq1 * t)
    tom2 = np.sin(2 * np.pi * freq2 * t)

    # Somar os dois tons
    tom = tom1 + tom2

    # Normalizar o tom para evitar clipping
    tom = tom / np.max(np.abs(tom))

    # Reproduzir o som
    print("Executando as senoides (emitindo o som)")
    sd.play(tom, fs)
    sd.wait()

    # Plotar o sinal no domínio do tempo
    plt.figure(figsize=(10, 4))
    plt.plot(t[0:500], tom[0:500])  # Plotando apenas as primeiras 500 amostras
    plt.title("Sinal no Domínio do Tempo")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    # Plotar o sinal no domínio da frequência
    print("Plotando a Transformada de Fourier")
    signal.plotFFT(tom, fs)

    # Exibir os gráficos
    plt.show()

if __name__ == "__main__":
    main()
