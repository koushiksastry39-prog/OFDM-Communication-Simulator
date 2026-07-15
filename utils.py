import numpy as np

def generate_bits(n):

    return np.random.randint(0,2,n)


def calculate_ber(original_bits, received_bits):

    errors = np.sum(original_bits != received_bits)

    ber = errors / len(original_bits)

    return ber, errors