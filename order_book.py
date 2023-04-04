from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    #Your code here
    new_order = Order(
        buy_currency=order['buy_currency'],
        sell_currency=order['sell_currency'],
        buy_amount=order['buy_amount'],
        sell_amount=order['sell_amount'],
        sender_pk=order['sender_pk'],
        receiver_pk=order['receiver_pk']
    )
    session.add(new_order)
    session.commit()


    orders = session.query(Order).filter(Order.filled == None).all()
    for existing_order in orders:
        if ((existing_order.buy_currency != new_order.sell_currency)
            or (existing_order.sell_currency != new_order.buy_currency)
            or (existing_order.sell_amount / existing_order.buy_amount < new_order.buy_amount / new_order.sell_amount)
            or (existing_order.counterparty_id != None)):
            continue
   
        match_order = existing_order

        match_order.filled = datetime.now()
        new_order.filled = datetime.now()
        match_order.counterparty_id = new_order.id
        new_order.counterparty_id = match_order.id
        session.commit()


        # If match_order is not completely filled
        if (new_order.sell_amount < match_order.buy_amount):
            diff = match_order.buy_amount - new_order.sell_amount
            exchange_rate_match = match_order.sell_amount / match_order.buy_amount
            sell_amount_new_match = diff * exchange_rate_match

            new_order = Order(sender_pk=match_order.sender_pk,
                              receiver_pk=match_order.receiver_pk,
                              buy_currency=match_order.buy_currency,
                              sell_currency=match_order.sell_currency,
                              buy_amount=diff,
                              sell_amount=sell_amount_new_match,
                              creator_id=match_order.id)
            session.add(new_order)
            session.commit()
    

        # If current_order is not completely filled
        if (new_order.buy_amount > match_order.sell_amount):
 
            diff = new_order.buy_amount - match_order.sell_amount
            exchange_rate_current = new_order.buy_amount / new_order.sell_amount
            sell_amount_new_current = diff / exchange_rate_current

            new_order = Order(sender_pk=new_order.sender_pk,
                              receiver_pk=new_order.receiver_pk,
                              buy_currency=new_order.buy_currency,
                              sell_currency=new_order.sell_currency,
                              buy_amount=diff,
                              sell_amount=sell_amount_new_current,
                              creator_id=new_order.id)
            session.add(new_order)
            session.commit()
        break
