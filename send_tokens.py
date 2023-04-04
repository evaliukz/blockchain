#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic, encoding
from algosdk import transaction
from algosdk import account

#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}


acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance


# generate an account
#private_key, address = account.generate_account()
#print(f"address: {address}")
#print(f"private key: {private_key}")
#print(f"mnemonic: {mnemonic.from_private_key(private_key)}")

# check if the address is valid
#if encoding.is_valid_address(address):
#    print("The address is valid!")
#else:
#    print("The address is invalid.")

mnemonic_secret = "flip funny month typical tilt electric luxury topic upper laugh wrist puppy service idea private shift reject neither minor unfair empower spawn small abstract audit"
sk = mnemonic.to_private_key(mnemonic_secret)
sender_pk = mnemonic.to_public_key(mnemonic_secret)

#print("Private key:", sk)
#print("Address:", sender_pk)

# check the address
if encoding.is_valid_address(sender_pk):
    print("valid!")
else:
    print("invalid.")

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here
    #create transaction
    tx = transaction.PaymentTxn(sender_pk, tx_fee, first_valid_round, last_valid_round, gen_hash, receiver_pk, tx_amount)
    #sign
    signed_tx = tx.sign(sk)
    #send
    txid = acl.send_transaction(signed_tx)
    wait_for_confirmation(acl, txid)
    return sender_pk, txid

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

