import numpy as np

def bpsk_modulate(bits):

    return np.where(bits == 0, -1, 1)


def bpsk_demodulate(symbols):

    bits = np.where(symbols.real >= 0, 1, 0)

    return bits