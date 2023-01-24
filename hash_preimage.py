import hashlib
import os
import random
import string


def hash_preimage(target_string):
    if not all([x in '01' for x in target_string]):
        print("Input should be a string of bits")
        return
    x = b'\x00'
    # target_bit = target_string.encode('utf-8')
    k = len(target_string)
    x = random.choice(string.ascii_letters)
    x_sha = hashlib.sha256(x.encode('utf-8'))
    final_k_digits_x = bin(int(x_sha.hexdigest(), base=16))[-k:]

    while final_k_digits_x != target_string:
        x += random.choice(string.ascii_letters)
        x_sha = hashlib.sha256(x.encode('utf-8'))
        final_k_digits_x = bin(int(x_sha.hexdigest(), base=16))[-k:]

    return x