import random

from params import p
from params import g

# To encrypt m , generate a random r in the range 1≤r≤q , and set
# (c1,c2)=(g^r mod p, h^r⋅m mod p)

# The function “keygen” should take no arguments and return a secret key (an integer in the range 1,…,p) 
# and a public key g^a mod p

def keygen():
    sk = random.randint(1, p)
    pk = pow(g, sk, p)
    return pk,sk

# The function “encrypt” should take a public key h , and an integer  m  and return an El Gamal ciphertext.
def encrypt(pk,m):
    r = random.randint(1, p)
    c1 = pow(g, r, p) # pow(number, power, modulus [optional])
    c2 = ( (m % p) * pow(pk, r, p) ) % p
    return [c1, c2]

# Given a ciphertext, (c1,c2) , and a secret key a , set m=c2 / ca1 mod p 
def decrypt(sk,c):
    c1 = c[0]
    c2 = c[1]
    m = ( (c2 % p) * pow(c1, -sk, p) ) % p
    return m
