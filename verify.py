from web3 import Web3
from eth_account.messages import encode_defunct
import random

def signChallenge( challenge ):

    w3 = Web3()
    #acc = w3.eth.account.create()
    #print(f'private key={w3.toHex(acc.privateKey)}, account={acc.address}')
    #private key=0x67b5360a59a1984ab9b803802b4a54dbd11cd8bcdb6471924a29df071a17e905, account=0xA96cC25F68D6b852a813169b8224a04be9F06E80
    #Transaction: https://testnet.snowtrace.io/tx/0xae0c0e35a8d562de324a9168d69af5fbd9b890c6c8275bd0d55f9bab9f772c77
    
    #This is the only line you need to modify
    sk = "0x67b5360a59a1984ab9b803802b4a54dbd11cd8bcdb6471924a29df071a17e905"

    acct = w3.eth.account.from_key(sk)


    signed_message = w3.eth.account.sign_message( challenge, private_key = acct._private_key )

    return acct.address, signed_message.signature


def verifySig():
    """
        This is essentially the code that the autograder will use to test signChallenge
        We've added it here for testing 
    """

    challenge_bytes = random.randbytes(32)

    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge( challenge )

    w3 = Web3()

    return w3.eth.account.recover_message( challenge , signature=sig ) == address

if __name__ == '__main__':
    """
        Test your function
    """
    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )

