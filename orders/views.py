from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import simplejson

from settings import dao

from orders.forms import SectionForm, ItemForm, ItemInsert



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
"""
def managerview(request, client_id):
    #TODO: some refactoring,
    #      make the form validations work with the javascript part
    menu = dao.get_client_menu(client_id)
    items = dao.get_client_items(client_id)
    if request.method == 'POST':
        if 'add_section' in request.POST:
            #This case handles the add section submit form
            section_form = SectionForm(request.POST)
            item_form = ItemForm()
            iteminsert_form = ItemInsert(choices=items)
            if section_form.is_valid():
                #If the form is valid it enters here
                cd = section_form.cleaned_data
                name = cd['name']
                has_subsections = cd['has_subsections']
                inside = cd['inside']
                dao.add_section(client_id, name, has_subsections, inside)
        elif 'delete_section' in request.POST:
            #This case handles the delete section submit form
            section_form = SectionForm(request.POST)
            item_form = ItemForm()
            iteminsert_form = ItemInsert(choices=items)
            if section_form.is_valid():
                #If the form is valid it enters here
                cd = section_form.cleaned_data
                name = cd['name']
                inside = cd['inside']
                dao.del_section(client_id, name, inside)
        elif 'add_item' in request.POST:
            #This case handles de add items submit form
            section_form = SectionForm()
            item_form = ItemForm(request.POST)
            iteminsert_form = ItemInsert(choices=items)
            if item_form.is_valid():
                #If the form is valid it enters here
                cd = item_form.cleaned_data
                name = cd['name']
                price = cd['price']
                description = cd['description']
                if request.is_ajax():
                    #Checks if the request is ajax after the validation of the form
                    #Even though the javascript part is running without validation...
                    dao.add_item(client_id, name, price, description)
        elif 'delete_item_id' in request.POST:
            #This case handles de delete item submit form
            section_form = SectionForm()
            item_form = ItemForm()
            iteminsert_form = ItemInsert(choices=items)
            item_id = request.POST['delete_item_id']
            if request.is_ajax():
                #Checks if the request is ajax
                #IDK if this is necesary or even in the right order
                dao.del_item(item_id)
        elif 'insertitem' in request.POST:
            #This case handles de insert item submit form
            section_form = SectionForm()
            item_form = ItemForm()
            iteminsert_form = ItemInsert(request.POST, choices=items)
            if iteminsert_form.is_valid():
                #If the form is valid it enters here
                cd = iteminsert_form.cleaned_data
                insert = cd['insert']
                inside = cd['inside']
                dao.insert_item(client_id, insert, inside)
        elif 'remove_from' in request.POST:
            #This case handles de remove item submit form
            section_form = SectionForm()
            item_form = ItemForm()
            iteminsert_form = ItemInsert(request.POST, choices=items)
            if iteminsert_form.is_valid():
                #If the form is valid it enters here
                cd = iteminsert_form.cleaned_data
                insert = cd['insert']
                inside = cd['inside']
                dao.remove_item(client_id, insert, inside)
    else:
        #This case handles when request.method == GET
        #When the page is loaded the first time
        section_form = SectionForm()
        item_form = ItemForm()
        iteminsert_form = ItemInsert(choices=items)
    return render(request, 'desktop_index.html',
                  {'menu': menu, 'items': items,
                   'section_form': section_form,
                   'item_form': item_form,
                   'iteminsert': iteminsert_form,
                   'template': 'manager.html',
                   'title': 'Manager'})
"""
def manager_items(request, client_id):
    #TODO: some refactoring,
    #      make the form validations work with the javascript part
    menu = dao.get_client_menu(client_id)
    items = dao.get_client_items(client_id)
    if request.method == 'POST':
        if 'add_item' in request.POST:
            #This case handles de add items submit form
            item_form = ItemForm(request.POST)
            if item_form.is_valid():
                #If the form is valid it enters here
                cd = item_form.cleaned_data
                name = cd['name']
                price = cd['price']
                description = cd['description']
                if request.is_ajax():
                    #Checks if the request is ajax after the validation of the form
                    #Even though the javascript part is running without validation...
                    dao.add_item(client_id, name, price, description)
        elif 'delete_item_id' in request.POST:
            #This case handles de delete item submit form
            item_form = ItemForm()
            item_id = request.POST['delete_item_id']
            if request.is_ajax():
                #Checks if the request is ajax
                #IDK if this is necesary or even in the right order
                dao.del_item(item_id)     
    else:
        #This case handles when request.method == GET
        #When the page is loaded the first time
        item_form = ItemForm()
    return render(request, 'desktop_index.html',
                  {'items': items,
                   'item_form': item_form,
                   'template': 'manager_items.html',
                   'title': 'Manager'})

def manager_menus(request, client_id):
    #TODO: some refactoring,
    #      make the form validations work with the javascript part
    menu = dao.get_client_menu(client_id)
    items = dao.get_client_items(client_id)
    if request.method == 'POST':
        jstree_menu = jstree(menu)
        print "asd"
        if request.is_ajax():
            print "HELLO", request.POST
    else:
        #This case handles when request.method == GET
        #When the page is loaded the first time
        jstree_menu = jstree(menu)
        if request.is_ajax():
            print "HELLO GET"
            jstree2normal(request.GET)
    return render(request, 'desktop_index.html',
                  {'menu': menu, 'items': items,
                   'json_menu': simplejson.dumps(jstree_menu),
                   'template': 'manager_menus.html',
                   'title': 'Manager'})

def jstree(menu):
    tree = {'data': []}
    i = 0
    for section in menu['structure']:
        tree['data'].append({'data': section, 'children':[]})
        j = 0
        for subsection in menu['structure'][section]:
            tree['data'][i]['children'].append({'data': subsection, 'children':[]})
            for item in menu['structure'][section][subsection]:
                tree['data'][i]['children'][j]['children'].append(item)
            j += 1
        i += 1
    return tree

def jstree2normal(tree):
    print tree
    return tree
    

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

def order(request, order_id): 
    '''Displays order details and allows a server to update the status
    of the order. It extracts the definition of valid statii from the dao'''
    order = dao.get_order(order_id)
    statii = []
    for status in dao.ORDER_STATII:
        statii.append({'name':status.replace('_','').capitalize(), 'value':status})
    return render(request, 'index.html', 
                  {'template':'order.html', 'order':order, 'statii':statii})

def update_order(request, order_id):
    '''Updates the specified order with the params in the request'''
    print('update_order',order_id)
    status = request.POST['status']
    res = dao.update_order(order_id, status)
    if res != status:
        # TODO: return a 503?
        return
    client_id = dao.get_client_id(order_id)
    return render(request, 'index.html',
                  {'template':'updated.html', 'client_id':client_id})
