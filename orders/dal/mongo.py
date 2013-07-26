import pymongo

class OrdersDAO:
    '''This class defines the data access object to be used for data
    stored in MongoDB'''
    
    def __init__(self):
        self.client = pymongo.MongoClient()

    def get_menu(self,client_id=1):
        '''for now just get the first menu in the collection and
        ignore the specified client id'''
        menu = self.client.orders.menus.find_one()
        menu.pop('_id', None) # remove mongo id
        return menu

    def get_dish(self,dish_id=1):
        '''get the specified dish from the DB'''
        dish = self.client.orders.dishes.find_one()
        return dish
