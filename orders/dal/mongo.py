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

    def get_dish(self,item_id=1):
        '''get the specified dish from the DB'''
        print('get_dish',item_id)
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


class ManagerDAO:

    def __init__(self, client_name):
        self.client = pymongo.MongoClient()
        self.db = eval('self.client.' + str(client_name))
        if list(self.db.menu.find()) == []:
            self.db.menu.insert({'_id': 'menu'})

    def get_menu(self):
        return list(self.db.menu.find())

    def get_items(self):
        return list(self.db.items.find())

    def add_section(self, name, has_subsections, inside):
        if has_subsections:
            if inside:
                self.db.menu.update({'_id': 'menu'}, {'$set': { str(inside) + "." + str(name) : {} }})
            else:
                self.db.menu.update({'_id': 'menu'}, {'$set': { str(name) : {} }})
        else:
            if inside:
                self.db.menu.update({'_id': 'menu'}, {'$set': { str(inside) + "." + str(name) : [] }})
            else:
                self.db.menu.update({'_id': 'menu'}, {'$set': { str(name) : [] }})

    def del_section(self, name, inside):
        if inside:
            self.db.menu.update({'_id': 'menu'}, {'$unset': {str(inside) + "." + str(name): [] }})
        else:
            self.db.menu.update({'_id': 'menu'}, {'$unset': {str(name): [] }})

    def add_item(self, name, price):
        self.db.items.insert({'name': name, 'price': price})

    def del_item(self, name):
        self.db.items.remove({'name': name})

    def insert_item(self, insert, inside):
        self.db.menu.update({'_id': 'menu'}, {'$addToSet': { str(inside) : str(insert)}})

    def remove_item_from(self, item, inside):
        self.db.menu.update({'_id': 'menu'}, {'$pull': {str(inside): str(item)}})

    
