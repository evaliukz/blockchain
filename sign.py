import hashlib
import random

from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256

# “sign" "takes in a single message m, and, creates a new key-pair for an ECDSA signature scheme,
# and signs the message m

def sign(m):

	#generate public key
	#Your code here
    key_pair = keys.gen_keypair(curve.secp256k1)
    first = key_pair[0]
    public_key = key_pair[1]

	#generate signature
	#Your code here
    signed = ecdsa.sign(m, first, curve.secp256k1)
    r = signed[0]
    s = signed[1]

    assert isinstance(public_key, point.Point)
    assert isinstance(r, int)
    assert isinstance(s, int)
    return (public_key, [r, s])
