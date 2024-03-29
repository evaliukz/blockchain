#!/usr/bin/python3
from algosdk.v2client import algod
from algosdk.v2client import indexer
from algosdk import account
from algosdk.future import transaction


def connect_to_algo(connection_type=''):
    # Connect to Algorand node maintained by PureStake
    algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"

    if connection_type == "indexer":
        # TODO: return an instance of the v2client indexer. This is used for checking payments for tx_id's
        algod_address = "https://testnet-algorand.api.purestake.io/idx2"
    else:
        # TODO: return an instance of the client for sending transactions
        # Tutorial Link: https://developer.algorand.org/tutorials/creating-python-transaction-purestake-api/
        algod_address = "https://testnet-algorand.api.purestake.io/ps2"

    return None


def send_tokens_algo(acl, sender_sk, txes):
    params = acl.suggested_params

    # TODO: You might want to adjust the first/last valid rounds in the suggested_params
    #       See guide for details

    # TODO: For each transaction, do the following:
    #       - Create the Payment transaction
    #       - Sign the transaction

    # TODO: Return a list of transaction id's

    sender_pk = account.address_from_private_key(sender_sk)

    tx_ids = []
    for i, tx in enumerate(txes):
        unsigned_tx = tx

        # TODO: Sign the transaction
        signed_tx = unsigned_tx.sign(sender_pk)

        try:
            print(f"Sending {tx['amount']} microalgo from {sender_pk} to {tx['receiver_pk']}")

            # TODO: Send the transaction to the testnet

            tx_id = signed_tx.get_txid()
            tx_ids.append(tx_id)
            txinfo = wait_for_confirmation_algo(acl, txid=tx_id)
            print(f"Sent {tx['amount']} microalgo in transaction: {tx_id}\n")
        except Exception as e:
            print(e)

    return tx_ids


# !/usr/bin/python3

from algosdk.v2client import algod
from algosdk.v2client import indexer
from algosdk import account
from algosdk.future import transaction
import time


def connect_to_algo(connection_type=''):
    # Connect to Algorand node maintained by PureStake
    algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"

    headers = {"X-API-Key": algod_token}

    if connection_type == "indexer":
        # TODO: return an instance of the v2client indexer. This is used for checking payments for tx_id's
        algod_address = "https://testnet-algorand.api.purestake.io/idx2"
        myindexer = indexer.IndexerClient("", algod_address, headers)

        return myindexer

    else:
        # TODO: return an instance of the client for sending transactions
        # Tutorial Link: https://developer.algorand.org/tutorials/creating-python-transaction-purestake-api/
        algod_address = "https://testnet-algorand.api.purestake.io/ps2"
        algodClient = algod.AlgodClient(algod_token, algod_address, headers)

    return algodClient


def send_tokens_algo(acl, sender_sk, txes):
    params = acl.suggested_params()

    # TODO: You might want to adjust the first/last valid rounds in the suggested_params
    #       See guide for details

    # TODO: For each transaction, do the following:
    #       - Create the Payment transaction
    #       - Sign the transaction

    # TODO: Return a list of transaction id's

    sender_pk = account.address_from_private_key(sender_sk)
    tx_ids = []
    txes1 = []
    for i, tx in enumerate(txes):
        receiver_address = tx['receiver_pk']
        amount = tx['amount']

        unsigned_tx = transaction.PaymentTxn(sender_pk, params, receiver_address, amount)
        # TODO: Sign the transaction
        signed_tx = unsigned_tx.sign(sender_sk)

        try:
            print(f"Sending {tx['amount']} microalgo from {sender_pk} to {tx['receiver_pk']}")

            tx_confirm = acl.send_transaction(signed_tx)

            # TODO: Send the transaction to the testnet

            tx_id = signed_tx.transaction.get_txid()
            time.sleep(5)
            txinfo = wait_for_confirmation_algo(acl, txid=tx_id)
            # params.first += 1
            tx_ids.append(tx_id)
            tx['tx_id'] = tx_id
            txes1.append(tx)
            print(f"Sent {tx['amount']} microalgo in transaction: {tx_id}\n")

        except Exception as e:
            print(e)

    return txes1


# Function from Algorand Inc.
def wait_for_confirmation_algo(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        time.sleep(5)
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo


##################################

from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import TransactionNotFound
import json
import progressbar


def connect_to_eth():
    IP_ADDR = '3.23.118.2'  # Private Ethereum
    PORT = '8545'

    w3 = Web3(Web3.HTTPProvider('http://' + IP_ADDR + ':' + PORT))
    w3.middleware_onion.inject(geth_poa_middleware,
                               layer=0)  # Required to work on a PoA chain (like our private network)
    w3.eth.account.enable_unaudited_hdwallet_features()
    if w3.isConnected():
        return w3
    else:
        print("Failed to connect to Eth")
        return None


def wait_for_confirmation_eth(w3, tx_hash):
    print("Waiting for confirmation")
    widgets = [progressbar.BouncingBar(marker=progressbar.RotatingMarker(), fill_left=False)]
    i = 0
    with progressbar.ProgressBar(widgets=widgets, term_width=1) as progress:
        while True:
            i += 1
            progress.update(i)
            try:
                receipt = w3.eth.get_transaction_receipt(tx_hash)
            except TransactionNotFound:
                continue
            break
    return receipt


####################
def send_tokens_eth(w3, sender_sk, txes):
    sender_account = w3.eth.account.privateKeyToAccount(sender_sk)
    sender_pk = sender_account._address

    # TODO: For each of the txes, sign and send them to the testnet
    # Make sure you track the nonce -locally-
    starting_nonce = w3.eth.get_transaction_count(sender_pk, "pending")
    tx_ids = []
    txes1 = []
    for i, tx in enumerate(txes):
        # print(w3.eth.get_balance(sender_pk))
        tx_dict = {
            'nonce': starting_nonce + i,  # Locally update nonce
            'gasPrice': w3.eth.gas_price,
            'gas': w3.eth.estimate_gas(
                {'from': sender_pk,
                 'to': tx['receiver_pk'],
                 'data': b'',
                 'amount': tx['amount']}),
            'to': tx['receiver_pk'],
            'value': tx['amount'],
            'data': b''}

        signed_txn = w3.eth.account.sign_transaction(tx_dict, sender_sk)
        tx_id = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txinfo = wait_for_confirmation_eth(w3, tx_id)
        tx_ids.append(tx_id)
        tx['tx_id'] = tx_id
        txes1.append(tx)
        print(f"Sent {tx['amount']} eth in transaction: {tx_id}\n")

    return txes1
