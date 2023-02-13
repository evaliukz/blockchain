import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE
	json_object = json.dumps(data)
	files = {
    		'file': json_object
	}
	projectId = "2Lg7X9YNSBEdWfNq3VRE3f1uI34"
	projectSecret = "a87e6f9d49f89f698cfbb14062e99697"
	response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files=files, auth=(projectId,projectSecret))
	cid=response.json()['Hash']
	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	#YOUR CODE HERE	
	params = (
   	('arg', cid),
	)
	projectId = "2Lg7X9YNSBEdWfNq3VRE3f1uI34"
	projectSecret = "a87e6f9d49f89f698cfbb14062e99697"

	response = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params,  auth=(projectId,projectSecret))
	data = json.loads(response.text)

	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
