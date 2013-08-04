from django.http import HttpResponse
from django.shortcuts import render

from settings import dao

def menu(request, client_id):
    try:
        menu = dao.get_client_menu(client_id)
    except ValueError:
        print('invalid client id '+client_id)
        menu = dao.get_client_menu()
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

def place_order(request, item_id, client_id):
    '''Places an order for qty units of item_id from client_id. This
    should add the order to the DB, show the user a confirmation
    message and redirect them to the previous section they were
    browsing'''
    # TODO: orders should have a seat_id and an array of
    # events. quantity should come via a POST request
    quantity = request.GET['quantity']
    print('place_orders', item_id, client_id, quantity)
    dao.add_order(client_id, item_id, quantity)
    item_name = dao.get_item(item_id)['name']
    return render(request, 'index.html',
                  {'template':'confirmation.html', 'client':client_id, 'qty':quantity, 
                   'item_name':item_name})

def list_orders(request, client_id, query={}):
    '''Lists orders in the specified client's queue. It defaults to
    the pending orders, but the view should provide a way for the
    server or manager to filter by any combination of date, status and
    seat'''
    # TODO: implement the filters mentioned above
    orders = dao.list_orders(client_id, query)
    client_name = dao.get_client(client_id)['name']
    return render(request, 'index.html',
                  {'template':'orders.html', 'client_name':client_name,
                   'orders':orders})
