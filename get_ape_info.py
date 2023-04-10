from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = "https://cosmopolitan-holy-bridge.ethereum-sepolia.discover.quiknode.pro/ca045f298289774272dc5cb5853980e09266521e/"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	data = {'owner': "", 'image': "", 'eyes': "" }
	
	#YOUR CODE HERE	
	#contract=web3.eth.contract(address=contract_address,abi=abi)
    owner="0x46EFbAedc92067E6d60E84ED6395099723252496"

    # Get metadata from ifps.io
    ipfs_url = 'https://ipfs.io/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/'
    ape_id = str(apeID)
    ape_url = ipfs_url + ape_id
    response = requests.get(ape_url)
    content = response.content
    dictionary = json.loads(content.decode('utf-8'))
    image_url = dictionary['image']
    eye_index = 0
    for x in range(20):
        if dictionary['attributes'][x]['trait_type'] == 'Eyes':
            eye_index = x
            break
    eyes = dictionary['attributes'][eye_index]['value']
    response.close()

    data['owner']=owner
    data['eyes'] = eyes
    data['image'] = image_url
    print(data)
    print(apeID)

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

