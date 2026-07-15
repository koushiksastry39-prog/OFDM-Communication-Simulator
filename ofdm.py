import numpy as np

def serial_to_parallel(symbols, subcarriers):

    length = len(symbols)

    extra = length % subcarriers

    if extra != 0:

        padding = subcarriers - extra

        symbols = np.append(symbols, np.zeros(padding))

    parallel = symbols.reshape(-1, subcarriers)

    return parallel


def ofdm_modulate(parallel):

    return np.fft.ifft(parallel, axis=1)


def add_cyclic_prefix(ofdm_signal, cp_length):

    cp = ofdm_signal[:, -cp_length:]

    return np.hstack((cp, ofdm_signal))
def remove_cyclic_prefix(signal, cp_length):

    return signal[:, cp_length:]


def ofdm_demodulate(received_signal):

    return np.fft.fft(received_signal, axis=1)

    return np.hstack((cp, ofdm_signal))