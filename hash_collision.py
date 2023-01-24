import hashlib
import string
import random

def hash_collision(k):
    if not isinstance(k,int):
        print( "hash_collision expects an integer" )
        return( b'\x00',b'\x00' )
    if k < 0:
        print( "Specify a positive number of bits" )
        return( b'\x00',b'\x00' )
   
    #Collision finding code goes here
    ascii_letters = string.ascii_letters
    x = ''.join(random.choice(ascii_letters) for i in range(256)).encode('utf-8')
    y = ''.join(random.choice(ascii_letters) for i in range(256)).encode('utf-8')
    
    isCollision = 0
    while (isCollision == 0):
        shaX = hashlib.sha256(x).digest()
        shaY = hashlib.sha256(y).digest()
        binaryX = bin(int.from_bytes(shaX, 'big'))
        binaryY = bin(int.from_bytes(shaY, 'big'))
        if (binaryX[(len(binaryX)-k):] == binaryY[(len(binaryY)-k):]):
            isCollision = 1
        else:
            strY = ''.join(random.choice(ascii_letters) for i in range (256))
            y = strY.encode('utf-8')
    return (x, y)
