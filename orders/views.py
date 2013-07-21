from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader

def menu(request):
    menu = {'Food':['Appetizers', 'Main Dishes', 'Desserts'], 'Drinks':['Sodas','Juices', 'Wines', 'Beers', 'Cocktails']}
    return render(request, 'menu.html', {'menu':menu})
