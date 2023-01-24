import hashlib
import string
import random

def hash_preimage(target_string):
    if not all( [x in '01' for x in target_string ] ):
        print( "Input should be a string of bits" )
        return
    nonce = b'\x00'

    length = len(target_string)
    
    # create a random string
    random_string = random.choice(string.ascii_letters)
    # get sha256 value and convert to binary
    random_string_sha = hashlib.sha256(random_string.encode('utf-8')) # convert the string to byte
    random_string_sha_binary = bin(int(random_string_sha .hexdigest(), base=16))[-length:]
    # compare string_sha_binary with target_string byte
    while random_string_sha_binary != target_string:
        nonce += random.choice(string.ascii_letters)
        random_string_sha = hashlib.sha256(nonce.encode('utf-8'))
        random_string_sha_binary = bin(int(random_string_sha.hexdigest(), base=16))[-length:]

    return nonce
