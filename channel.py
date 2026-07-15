import numpy as np

def awgn(signal, snr_db):

    signal_power = np.mean(np.abs(signal)**2)

    snr_linear = 10**(snr_db/10)

    noise_power = signal_power / snr_linear

    noise = np.sqrt(noise_power/2) * (
        np.random.randn(*signal.shape)
        +
        1j*np.random.randn(*signal.shape)
    )

    return signal + noise