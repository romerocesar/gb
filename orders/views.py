from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
import pymongo

TEST_MENU = {'Food':['Appetizers', 'Main Dishes', 'Desserts'], 'Drinks':['Sodas','Juices', 'Wines', 'Beers', 'Cocktails']} 

mongodb_client = pymongo.MongoClient()

def menu(request):
    menu = mongodb_client.test.menus.find_one()
    menu.pop('_id',0) # remove the document id added by mongo
    return render(request, 'menu.html', {'menu':menu})
