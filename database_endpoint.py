from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine, select, MetaData, Table
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only

from models import Base, Order, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

#These decorators allow you to use g.session to access the database inside the request code
@app.before_request
def create_session():
    g.session = scoped_session(DBSession) #g is an "application global" https://flask.palletsprojects.com/en/1.1.x/api/#application-globals

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    g.session.commit()
    g.session.remove()

"""
-------- Helper methods (feel free to add your own!) -------
"""

def log_message(d)
    # Takes input dictionary d and writes it to the Log table
    pass

"""
---------------- Endpoints ----------------
"""
    
@app.route('/trade', methods=['POST'])
def trade():
    if request.method == "POST":
        content = request.get_json(silent=True)
        print( f"content = {json.dumps(content)}" )
        columns = [ "sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform" ]
        fields = [ "sig", "payload" ]
        error = False
        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
        
        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            log_message(content)
            return jsonify( False )
            
        #Your code here
        #Note that you can access the database session using g.session
        #Get json contents
        sig = content['sig']
        payload = content['payload']
        pk = content['payload']['sender_pk']
        platform = content['payload']['platform']
        payload_json = json.dumps(payload)

        # The platform must be either “Algorand” or "Ethereum".
        platforms = ["Algorand", "Ethereum"]
        if not platform in platforms:
            print("platform is not Algorand or Ethereum")
            return jsonify(False)

        #The platform must be either “Algorand” or "Ethereum". 
        #Your code should check whether “sig” is a valid signature of json.dumps(payload), 
        #using the signature algorithm specified by the platform field. 
        #Be sure to verify the payload using the sender_pk.
        result = False

        if platform == "Algorand":
            #print("platform is Algorand")
            if algosdk.util.verify_bytes(payload_json.encode('utf-8'), sig, pk):
                print("Algorand sig verified!")
                result = True

        elif platform == "Ethereum":
            #print("platform is Ethereum")
            eth_encoded_msg = eth_account.messages.encode_defunct(text=payload_json)
            if eth_account.Account.recover_message(eth_encoded_msg, signature=sig) == pk:
                print("Ethereum sig verified!")
                result = True
        
        # In this assignment, you will not need to match or fill the orders,
        # simply insert them into the database (if the signature verifies).

        # If the signature verifies, store the signature,
        # as well as all of the fields under the ‘payload’ in the “Order” table EXCEPT for 'platform’.
        if result is True:
            print("signature verified")
            create_session()
            order_obj = Order(sender_pk=payload['sender_pk'],
                              receiver_pk=payload['receiver_pk'],
                              buy_currency=payload['buy_currency'],
                              sell_currency=payload['sell_currency'],
                              buy_amount=payload['buy_amount'],
                              sell_amount=payload['sell_amount'],
                              signature=sig)            
            g.session.add(order_obj)
            shutdown_session()
            return jsonify(result)

        # If the signature does not verify, do not insert the order into the “Order” table.
        # Instead, insert a record into the “Log” table, with the message field set to be json.dumps(payload).
        if result is False:
            print("signature was not verified")
            log_message(payload_json)            
            return jsonify(result)


@app.route('/order_book')
def order_book():
    #Your code here
    #Note that you can access the database session using g.session
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
