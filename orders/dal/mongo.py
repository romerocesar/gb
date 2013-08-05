import os
import pymongo
from bootstrap import menus, items, clients

class OrdersDAO:
    '''This class defines the data access object to be used for data
    stored in MongoDB'''
    
    def __init__(self, bootstrap=False):
        self.client = pymongo.MongoClient()
        self.db = self.client.orders
        if bootstrap:
            # load bootstrap data
            self.db.clients.remove()
            self.db.clients.insert(clients)
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

    def get_active_menu(self, client_id):
        return self.db.clients.find_one({'_id': client_id})['menu']

    def m_get_menu(self, client_id):
        menu_id = self.db.clients.find_one({'_id': client_id})['menu']
        menu = self.db.menus.find_one({'_id': menu_id})
        return menu

    def m_get_items(self, client_id):
        items = list(self.db.items.find({'client_id': client_id}))
        return items

    def add_item(self, client_id, name, price, description):
        self.db.items.insert({'client_id': client_id,
                              'name': name,
                              'price': price,
                              'description': description})

    def del_item(self, client_id, name):
        self.db.items.remove({'client_id': client_id,
                              'name': name})

    def add_section(self, client_id, name, has_subsections, inside):
        menu_id = self.get_active_menu(client_id)
        if has_subsections:
            if inside:
                self.db.menus.update({'_id': menu_id}, {'$set': { "structure." + str(inside) + "." + str(name) : {} }})
            else:
                self.db.menus.update({'_id': menu_id}, {'$set': { "structure." + str(name) : {} }})
        else:
            if inside:
                self.db.menus.update({'_id': menu_id}, {'$set': { "structure." + str(inside) + "." + str(name) : [] }})
            else:
                self.db.menus.update({'_id': menu_id}, {'$set': { "structure." + str(name) : [] }})

    def del_section(self, client_id, name, inside):
        menu_id = self.get_active_menu(client_id)
        if inside:
            self.db.menus.update({'_id': menu_id}, {'$unset': { "structure." + str(inside) + "." + str(name): [] }})
        else:
            self.db.menus.update({'_id': menu_id}, {'$unset': { "structure." + str(name): [] }})

    def insert_item(self, client_id, insert, inside):
        menu_id = self.get_active_menu(client_id)
        self.db.menus.update({'_id': menu_id}, {'$addToSet': { "structure." + str(inside) : str(insert)}})

    def remove_item_from(self, client_id, item, inside):
        menu_id = self.get_active_menu(client_id)
        self.db.menus.update({'_id': menu_id}, {'$pull': { "structure." + str(inside): str(item)}})


    
