import logging
import os
import pymongo
import datetime

from bson.objectid import ObjectId
from bootstrap import menus, items, clients
from orders import OrdersDAO

logger = logging.getLogger('orders.mongo')

class MongoOrdersDAO(OrdersDAO):
    '''This class defines the data access object to be used for data
    stored in MongoDB'''

    def __init__(self, bootstrap=False):
        self.client = pymongo.MongoClient()
        self.db = self.client.orders
        if bootstrap:
            # load bootstrap data
            self.db.menus.remove()
            self.db.menus.insert(menus)
            self.db.items.remove()
            self.db.items.insert(items)
            self.db.clients.remove()
            self.db.clients.insert(clients)

    def get_menu(self, menu_id):
        '''Gets the menu that matches the specified menu ID'''
        logger.debug('menu_id: %s', menu_id)
        mongoid = get_mongo_id(menu_id)
        menu = self.db.menus.find_one(mongoid)
        menu['id'] = str(menu['_id'])
        logger.info('menu:%s', menu)
        return menu

    def get_client_menus_list(self, client_id):
        '''Gets the list of menus from the client'''
        return self.db.clients.find_one({'_id': client_id})['menus']

    def get_client_menus(self, client_id):
        '''Gets all the content of all the menus of the client'''
        menus_list = self.get_client_menus_list(client_id)
        menus = []
        for menu in menus_list:
            if len(menu) > 10:
                #Mongo id
                menus.append(self.db.menus.find_one({'_id': ObjectId(menu)}))
            else:
                #Bootstrapped id
                menus.append(self.db.menus.find_one({'_id': menu}))
            menus[-1]['id'] = str(menus[-1]['_id'])
        return menus
    
    def get_item(self,item_id=1):
        '''get the specified item from the DB'''
        logger.debug('item_id: %s',item_id)
        if len(item_id) > 10:
            #Mongo id
            item = self.db.items.find_one({'_id':ObjectId(item_id)})
        else:
            #Bootstrapped id
            item = self.db.items.find_one({'_id':item_id})
        item['id'] = item['_id']
        logger.info('item %s',item)
        return item

    def get_items(self, ids):
        '''get a list of menu items that corresponds to the specified
        ids. If an id is invalid, it will be skipped silently so that
        other valid items can still be retrieved'''
        logger.debug('getting %d items: %s', len(ids), ids)
        mongoids = [get_mongo_id(i) for i in ids]
        logger.debug('fetching %d items from mongo %s',len(mongoids), mongoids)
        items  = self.db.items.find({'_id':{'$in':mongoids}})
        res = []
        for item in items:
            item['id'] = str(item['_id'])
            res.append(item)
        logger.info('got %d items %s', len(res), res)
        return res

    def get_client(self, client_id):
        '''Simply return the client that matches the specified id'''
        # TODO: should log an error if client id doens't exist.
        return self.db.clients.find_one(client_id)

    def get_client_id(self, order_id):
        'Return the client id the specified order belongs to'
        # TODO: what if order_id does not exist or it doesn't contain a client id?
        cid = self.db.orders.find_one(ObjectId(order_id))['client_id']
        return cid

    def get_active_menu_id(self, client_id):
        '''gets the id of the active menu of the client'''
        mongoid = get_mongo_id(client_id)
        return self.db.clients.find_one({'_id': mongoid})['menu']

    def get_active_menu(self, client_id):
        '''Gets the active menu for the specified client ID.'''
        logger.debug('client_id: %s',client_id)
        mongoid = get_mongo_id(client_id)
        mid = self.db.clients.find_one(mongoid)['menu']
        menu = self.db.menus.find_one(mid)
        menu['id'] = str(menu['_id'])
        logger.info('menu:%s',menu)
        return menu

    def get_client_name(self, client_id):
        return self.db.clients.find_one(client_id)['name']

    def get_client_items(self, client_id):
        items = list(self.db.items.find({'client_id': client_id}))
        for item in items:
            item['id'] = str(item['_id'])
        return items

    def add_item(self, client_id, name, price, description):
        self.db.items.insert({'client_id': client_id,
                              'name': name,
                              'price': price,
                              'description': description})

    def add_menu(self, title, client_id):
        menu_id = self.db.menus.insert({'title': title, 'structure': {}})
        self.db.clients.update({'_id': client_id}, {'$addToSet': {'menus': str(menu_id)}})

    def del_item(self, client_id, item_id):
        '''Deletes items from the db and the structures of menus'''
        self.remove_item_from_client_menus_structure(client_id, item_id)
        if len(item_id) < 10:
            #this are bootstraped items
            self.db.items.remove({'_id': item_id})
        else:
            #this are items with id generated by mongo
            self.db.items.remove({'_id': ObjectId(item_id)})

    def remove_item_from_client_menus_structure(self, client_id, item_id):
        '''Removes items from the structure of the menus of the client'''
        menus = self.get_client_menus(client_id)
        for menu in menus:
            menu_structure = str(menu['structure'])
            rcol = "u'%s'," % item_id
            lcol = ", u'%s'" % item_id
            last = "[u'%s']" % item_id
            if rcol in menu_structure:
                menu_structure = menu_structure.replace(rcol, '')
            if lcol in menu_structure:
                menu_structure = menu_structure.replace(lcol, '')
            if last in menu_structure:
                menu_structure = menu_structure.replace(last, '[]')
            menu_structure = eval(menu_structure)
            self.update_menu_structure(str(menu['_id']), menu_structure)
        
    def add_section(self, client_id, name, has_subsections, inside):
        '''adds a new section to the active menu of the client
        name(string) = name of the section to insert,
        has_subsection(boolean) = True if its going to have subsections inside,
                                  False if its going to have items inside,
        inside(string) = where inside the menu structure is going to add the section'''
        #TODO: make it work with any chosen menu, not only the active menu,
        #   find a generic way to set the 'path' of the item to be inserted
        menu_id = self.get_menu_id(client_id)
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
        '''deletes a section from the menu structure
        name(string) = name of the section to be deleted,
        inside(string) = path of the section to be deleted'''
        #TODO: make it work with any chosen menu, not only the active menu,
        #   find a generic way to set the 'path' of the item to be inserted
        menu_id = self.get_menu_id(client_id)
        if inside:
            self.db.menus.update({'_id': menu_id}, {'$unset': { "structure." + str(inside) + "." + str(name): [] }})
        else:
            self.db.menus.update({'_id': menu_id}, {'$unset': { "structure." + str(name): [] }})

    def insert_item(self, client_id, item_id, section):
        '''puts a item inside a section in the menu structure
        item_id(string) = id of the item to be inserted
        section(string) = path of the section where the item is going to be inserted'''
        #TODO: make it work with any chosen menu, not only the active menu,
        #   find a generic way to set the 'path' of the item to be inserted
        menu_id = self.get_menu_id(client_id)
        self.db.menus.update({'_id': menu_id}, {'$addToSet': { "structure." + str(section) : item_id}})

    def remove_item(self, client_id, item_id, section):
        '''pulls a item from a section
        item_id(string) = id of the item to be pulled
        section(string) = path of the section where the item is going to be pulled from'''
        #TODO: make it work with any chosen menu, not only the active menu,
        #   find a generic way to set the 'path' of the item to be inserted
        menu_id = self.get_menu_id(client_id)
        self.db.menus.update({'_id': menu_id}, {'$pull': { "structure." + str(section): item_id}})

    def add_order(self, item_id, quantity, client_id, seat_id):
        # TODO: Orders will need to have an array of events. Each
        # event will have a server_id, a timestamp and an action so
        # the order history can be traced and troubleshooted easily.
        logger.info({'item':item_id, 'qty':quantity, 'client':client_id, 'seat':seat_id})
        order = {'client_id':client_id, 'seat_id':seat_id, 'item_id':item_id, 'quantity':quantity,
                 'status':self.ORDER_PLACED}
        return self.db.orders.insert(order)

    def list_orders(self, client_id, query={}):
        '''Lists orders for the specified client matched by the given
        query. If query is not given, all orders in _placed_ status
        for the given client will be returned'''
        logger.debug('client_id: %s, query: %s', client_id, query)
        # TODO: move all field names to variables so this won't have
        # to change so dramatically whenever there's a schema change
        query['client_id'] = get_mongo_id(client_id)
        if 'status' in query and type(query['status']) in (tuple, list):
            query['status'] = {'$in':query['status']}
        orders = self.db.orders.find(query)
        res = []
        names = {}
        for order in orders:
            order['id'] = str(order['_id'])
            iid = order['item_id']
            if iid in names:
                order['item_name'] = names[iid]
            else:
                order['item_name'] = names[iid] = self.get_item_name(iid)
            order['delay'] = compute_delay(order)
            res.append(order)
        logger.info('orders: %s',res)
        return res

    def get_item_name(self, item_id):
        'Simply get the item name for the given item ID'
        logger.info('item_id: %s', item_id)
        ans = self.db.items.find_one(item_id)['name']
        logger.info('name: %s', ans)
        return ans

    def get_order(self, order_id): 
        '''Returns the order object that matches the given id. Adds
        the name of the item in the order as well as its delay as
        these two are almost always needed'''
        oid = ObjectId(order_id) 
        order = self.db.orders.find_one(oid)
        order['item_name'] = self.get_item_name(order['item_id'])
        order['delay'] = compute_delay(order)
        order['id'] = str(order['_id'])
        return order

    def update_order(self, order_id, status):
        'Updates the status of the specified order. Returns the new status of the order.'
        res = self.db.orders.find_and_modify({'_id':ObjectId(order_id)},{'$set':{'status':status}}, new=True)
        return res['status']

    def update_orders(self, ids, **attributes):
        '''Updates multiple orders by updating their attributes as specified in the input dictionary.
        Returns the IDs of the orders that failed to be updated if any.'''
        logger.debug({'ids':ids,'attrs':attributes})
        oids = [ObjectId(i) for i in ids]
        res = self.db.orders.update({'_id':{'$in':oids}},{'$set':attributes}, multi=True)
        logger.info('updated {} orders. Errors: {}.'.format(res['n'], res['err']))
        return res

    def is_valid_seat(self, client_id, seat_id): 
        '''Returns whether the given seat id belongs the the given
        client id'''
        logger.info('client_id: %s, seat_id: %s', client_id, seat_id)
        try:
            seats = self.get_client(client_id)['seats']
        except Exception as e:
            logger.exception('Error validating seat',e)
            return False
        return seat_id in seats

    def update_menu_structure(self, menu_id, structure):
        'Updates de structure of the menu'
        if len(menu_id) >10:
            #Mongo id
            self.db.menus.update({'_id': ObjectId(menu_id)}, {'$set': {'structure': structure}})
        else:
            #Bootstrapped id
            self.db.menus.update({'_id': menu_id}, {'$set': {'structure': structure}})

    def update_menu_title(self, menu_id, title):
        'Updates de title of the menu'
        logger.debug({'menu_id':menu_id,'title':title})
        mongoid = get_mongo_id(menu_id)
        self.db.menus.update({'_id': mongoid}, {'$set': {'title': title}})

    def update_active_menu(self, client_id, menu_id):
        'Sets the new active menu'
        self.db.clients.update({'_id': client_id}, {'$set': {'menu': menu_id}})

    def update_item(self, item_id, name = 'name', price = 'price', description = 'description'):
        'Updates the item properties'
        if len(item_id) > 10:
            #Mongo id
            self.db.items.update({'_id': ObjectId(item_id)}, {'$set': {'name': name, 'price': price, 'description': description}})
        else:
            #Bootstrapped id
            self.db.items.update({'_id': item_id}, {'$set': {'name': name, 'price': price, 'description': description}})

# Helper methods. The functions below are not part of the 'interface'
# and need not be implemented by other OrdersDAO
# implementations. These are what would be 'private' and perhaps
# 'static' methods in other OO languages
def compute_delay(mongo_obj):
    '''Computes how long ago the given mongo document was stored
    in the DB. It extracts the timestamp from the object ID and
    compares with the current time to determine how many seconds
    ago the object was created. Returns a simple human readable
    string that shows how long ago in seconds, minutes, hours or
    days ago the object was created'''
    timestamp = int(str(mongo_obj['_id'])[:8],16)
    now = datetime.datetime.utcnow()
    delta = now - datetime.datetime.utcfromtimestamp(timestamp)
    secs = int(delta.total_seconds())
    units = ((24*60*60,' day'),(60*60,' hr'),(60,' min'),(1,' sec'))
    idx = 0
    while secs < units[idx][0]:
        idx += 1
    qty = secs // units[idx][0]
    ans = str(qty) + units[idx][1]
    if qty > 1: 
        ans += 's'
    return ans + ' ago'

def get_mongo_id(iid):
    logger.debug('id: %s',iid)
    try:
        mongo_id = ObjectId(iid)
    except pymongo.errors.InvalidId:
        logger.warn('could not convert id %s to ObjectId',iid)
        mongo_id = iid
    logger.info('mongo_id: %s',mongo_id)
    return mongo_id
