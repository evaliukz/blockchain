import hashlib
import os
import random
import string


def hash_preimage(target_string):
    if not all([x in '01' for x in target_string]):
        print("Input should be a string of bits")
        return
    nonce = b'\x00'
   
    k = len(target_string)
    nonce = random.choice(string.ascii_letters) 
    nonce_sha = hashlib.sha256(nonce.encode('utf-8')) #convert to byte and get sha
    nonce_sha_binary = bin(int(nonce_sha.hexdigest(), base=16))[-k:] #to binary

    while nonce_sha_binary != target_string: #compare the random to target string
        nonce += random.choice(string.ascii_letters)
        nonce_sha = hashlib.sha256(nonce.encode('utf-8'))  #convert to byte and get sha
        nonce_sha_binary = bin(int(nonce_sha.hexdigest(), base=16))[-k:]  #to binary

    return nonce