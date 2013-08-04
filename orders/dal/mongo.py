import os
import pymongo
from bootstrap import menus, items

class OrdersDAO:
    '''This class defines the data access object to be used for data
    stored in MongoDB'''

    # order statii
    ORDER_PLACED = '_placed_'
    ORDER_PREPARED = '_prepared_'
    ORDER_SERVED = '_served_'
    ORDER_PAID = '_paid_'
    ORDER_RETURNED = '_returned_'

    def __init__(self, bootstrap=False):
        self.client = pymongo.MongoClient()
        if bootstrap:
            # load bootstrap data
            self.db = self.client.orders
            self.db.menus.remove()
            self.db.menus.insert(menus)
            self.db.items.remove()
            self.db.items.insert(items)

    def get_menu(self,client_id=1):
        '''for now just get the first menu in the collection and
        ignore the specified client id'''
        menu = self.db.menus.find_one()
        return menu

    def get_item(self,item_id=1):
        '''get the specified item from the DB'''
        print('get_item',item_id)
        item = self.db.items.find_one({'_id':item_id})
        print('item',item)
        return item

    def get_items(self,ids):
        '''get a list of menu items that corresponds to the specified
        ids. If an id is invalid, it will be skipped silently so that
        other valid items can still be retrieved'''
        # TODO: change this to actually use the input list of ids
        print('get_items',ids)
        items  = self.db.items.find({'_id':{'$in':ids}})
        res = []
        for item in items:
            item['id'] = str(item['_id'])
            res.append(item)
        print('res',res)
        return res

    def add_order(self, client_id, item_id, quantity):
        # TODO: orders will need to have a seat_id and an array of
        # events. Each event will have a server_id, a timestamp and an
        # action so the order history can be traced and troubleshooted
        # easily.
        order = {'client_id':client_id, 'item_id':item_id, 'quantity':quantity,
                 'status':self.ORDER_PLACED}
        return self.db.orders.insert(order)

    
