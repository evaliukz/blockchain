import hashlib
import os
import random
import string

def generateRandomString():
    letters = string.ascii_letters
    string = ''.join(random.choice(letters) for i in range(10))
    return string


def hash_collision(k):
    # check k
    if not isinstance(k, int):
        print("hash_collision expects an integer")
        return (b'\x00', b'\x00')
    if k < 0:
        print("Specify a positive number of bits")
        return (b'\x00', b'\x00')

    # generate a random string, convert it bytecode and assign it to x
    x = generateRandomString().encode('utf-8')

    # get the sha256 hash value of the byte code
    hex_result_x_random = hashlib.sha256(x).hexdigest()

    bin_result_x_random = (bin(int(hex_result_x_random, 16))[2:]).zfill(256)

    # use a while loop to find y with brute force
    while True:
        # generate a random string
        # convert the str to bytecode and assign it to x
        y = generateRandomString().encode('utf-8')

        # get the sha256 hash value of the byte code
        hex_result_y_random = hashlib.sha256(y).hexdigest()

        bin_result_y_random = (bin(int(hex_result_y_random, 16))[2:]).zfill(256)

        # compare the last k digits
        if (bin_result_y_random[-k:] == bin_result_x_random[-k:]) :
            break

    return (x, y)
