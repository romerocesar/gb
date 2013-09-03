'''This is a Test data access object. It does not connect to any
database or provide real data, but rather just keeps objects in memory
to be used for testing or when the actual DB has not been setup in the
dev environment'''
from orders import OrdersDAO

class TestOrdersDAO(OrdersDAO):

    def __init__(self):
        self.menus = [{'Food':['Appetizers', 'Main Dishes', 'Desserts'],
                     'Drinks':['Sodas','Juices', 'Wines', 'Beers', 'Cocktails']}]

    def get_menu(self,client_id):
        return self.menus[0]
