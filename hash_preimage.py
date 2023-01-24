import hashlib
import string
import random

def hash_preimage(target_string):
    if not all( [x in '01' for x in target_string ] ):
        print( "Input should be a string of bits" )
        return
    nonce = b'\x00'

    len = len(target_string)
    ascii_letters = string.ascii_letters

    while True:
        # create a random string
        random_string = ''.join(random.choice(ascii_letters) for i in range(10))
        # get sha256 value and convert to binary
        random_string_sha = hashlib.sha256(random_string.encode('utf-8')) # convert the string to byte
        random_string_sha_hex = random_string_sha.hexdigest()
        random_string_sha_binary = (bin(int(random_string_sha_hex, 16))[2:]).zfill(256)
        # compare string_sha_binary with target_string byte
        if ( random_string_sha_binary[-len:] == target_string ):
            nonce = random_string.encode('utf-8')
            break

    return( nonce )
