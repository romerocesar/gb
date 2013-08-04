import os
import pymongo
from bootstrap import menus, items, clients

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
            self.db.clients.remove()
            self.db.clients.insert(clients)

    def get_client_menu(self, client_id='c0'):
        '''Gets the active menu for the specified client ID.'''
        mid = self.db.clients.find_one(client_id)['menu']
        menu = self.db.menus.find_one(mid)
        return menu

    def get_menu(self, menu_id='m0'):
        '''Gets the menu that matches the specified menu ID'''
        return self.db.menus.find_one(menu_id)
    
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

    def list_orders(self, client_id, query={}): 
        '''Lists orders for the specified client matched by the given
        query. If query is not given, all pending orders for the given
        client will be returned'''
        # TODO: actually use the given filter for the query.
        print('list_orders',client_id, query)
        orders = self.db.orders.find({'client_id':client_id})
        res = []
        names = {}
        for order in orders:
            order['id'] = order['_id']
            iid = order['item_id']
            if iid in names:
                order['item_name'] = names[iid]
            else:
                order['item_name'] = names[iid] = self.get_item_name(iid)
            res.append(order)
        print('orders',res)
        return res

    def get_item_name(self, item_id):
        'Simply get the item name for the given item ID'
        ans = self.db.items.find_one(item_id)['name']
        print('get_item_name',ans)
        return ans

    def get_client(self, client_id):
        '''Simply return the client that matches the specified id'''
        return self.db.clients.find_one(client_id)
