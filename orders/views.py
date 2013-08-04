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
    menu['id'] = str(menu['_id'])
    return render(request, 'index.html',
                  {'menu':menu, 'template':'menu.html', 'title':'Menu'})

def item(request, item_id):
    item = dao.get_item(item_id)
    item['id'] = item['_id']
    return render(request, 'index.html',
                 {'template':'item.html', 'title':item['name'], 'item':item})

def section(request, menu_id, division, section):
    print('section',menu_id,section)
    menu = dao.get_menu(menu_id)
    ids = menu['structure'][division][section]
    items = dao.get_items(ids)
    print('items ', items)
    return render(request, 'index.html',
                {'template':'section.html', 'name':section, 'items':items})

def place_order(request, qty, item_id, client_id):
    '''Places an order for qty units of item_id from client_id. This
    should add the order to the DB, show the user a confirmation
    message and redirect them to the previous section they were
    browsing'''
    # TODO: orders should have a seat_id and an array of events
    dao.add_order(client_id, item_id, qty)
    item_name = dao.get_item(item_id)['name']
    return render(request, 'index.html',
                  {'template':'confirmation.html', 'client':client_id, 'qty':qty, 
                   'item_name':item_name})
