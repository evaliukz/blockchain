from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
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

    for old_order in session.query(Order).filter(Order.filled == None).all():
            if old_order.sell_currency != new_order.buy_currency:
                continue
            if old_order.buy_currency != new_order.sell_currency:
                continue
            if old_order.sell_amount / old_order.buy_amount < new_order.buy_amount / new_order.sell_amount:
                continue
            old_order.filled = datetime.now()
            new_order.filled = datetime.now()
            old_order.counterparty_id = new_order.id
            new_order.counterparty_id = old_order.id
            session.commit()
            
    
            if new_order.buy_amount > old_order.sell_amount:
            
                new = Order(sender_pk = new_order.sender_pk,receiver_pk = new_order.receiver_pk, 
                                  buy_currency = new_order.buy_currency, sell_currency = new_order.sell_currency, 
                                  buy_amount = new_order.buy_amount - old_order.sell_amount, 
                                  sell_amount = (new_order.buy_amount - old_order.sell_amount)* new_order.sell_amount / new_order.buy_amount,
                                  creator_id = new_order.id)
                session.add(new)
                session.commit()

                                           
    
            if old_order.buy_amount > new_order.sell_amount:
                new = Order(sender_pk = old_order.sender_pk,receiver_pk = old_order.receiver_pk, 
                                  buy_currency =old_order.buy_currency, sell_currency = old_order.sell_currency, 
                                  buy_amount = old_order.buy_amount - new_order.sell_amount, 
                                  sell_amount= (old_order.buy_amount - new_order.sell_amount) * old_order.sell_amount / old_order.buy_amount,
                                  creator_id = old_order.id)
                session.add(new)
                session.commit()
            break