from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime

# connect to the RPC
rpcuser='quaker_quorum'
rpcpassword='franklin_fought_for_continental_cash'
rpcport=8332
rpcip='3.134.159.30'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpcuser, rpcpassword, rpcip, rpcport))

# get info about the first bitCoin block
first_block_hash = rpc_connection.getblockhash(1)
print(rpc_connection.getblock(first_block_hash))

# batch support : print timestamps of blocks 0 to 99
# run in 2 RPC round-trips
# example: https://github.com/jgarzik/python-bitcoinrpc
commands = [ [ "getblockhash", height] for height in range(1000) ]
block_hashes = rpc_connection.batch_(commands)
blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
block_times = [ block["time"] for block in blocks ]
# print
for i in range(len(block_times)):
    print(i)
    time = block_times[i]
    print(time)
    print(datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
