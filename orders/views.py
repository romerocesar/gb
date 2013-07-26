from django.http import HttpResponse
from django.shortcuts import render

from settings import dao

def menu(request, client_id):
    try:
        client_id = int(client_id)
        menu = dao.get_menu(client_id)
    except ValueError:
        print('invalid client id '+client_id)
        menu = dao.get_menu()

    return render(request, 'index.html',
                  {'menu':menu, 'template':'menu.html', 'title':'Menu'})

def dish(request, dish_id):
    dish = dao.get_dish(dish_id)
    return render(request, 'index.html',
                 {'template':'dish.html', 'title':dish['name'], 'dish':dish})
