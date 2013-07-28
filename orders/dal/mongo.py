import os
import pymongo
from bootstrap import menus, items

class OrdersDAO:
    '''This class defines the data access object to be used for data
    stored in MongoDB'''
    
    def __init__(self, bootstrap=False):
        self.client = pymongo.MongoClient()
        if bootstrap:
            # load bootstrap data
            db = self.client.orders
            db.menus.remove()
            db.menus.insert(menus)
            db.items.remove()
            db.items.insert(items)

    def get_menu(self,client_id=1):
        '''for now just get the first menu in the collection and
        ignore the specified client id'''
        menu = self.client.orders.menus.find_one()
        return menu

    def get_dish(self,item_id=1):
        '''get the specified dish from the DB'''
        print('get_dish',item_id)
        item = self.client.orders.items.find_one({'_id':item_id})
        print('item',item)
        return item

    def get_items(self,ids):
        '''get a list of menu items that corresponds to the specified
        ids. If an id is invalid, it will be skipped silently so that
        other valid items can still be retrieved'''
        # TODO: change this to actually use the input list of ids
        print('get_items',ids)
        items  = self.client.orders.items.find()
        res = []
        for item in items:
            item['id'] = str(item['_id'])
            res.append(item)
        print('res',res)
        return res
