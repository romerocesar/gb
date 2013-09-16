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
    items = dao.get_client_items_w_id(client_id)
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
                dao.del_item(client_id, item_id)     
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
    menus = dao.get_client_menus(client_id)
    items = dao.get_client_items_name_id(client_id)
    if request.method == 'POST':
        if request.is_ajax():
            if 'add_menu' in request.POST:
                "Adds new menu to the db"
                dao.add_menu(request.POST['menu_title'], client_id)
            elif 'save_menu' in request.POST:
                "Saves the selected menu to the db"
                #print jstree2mongo(request.POST)
                menu = jstree2mongo2(request.POST)
                dao.update_menu_title(menu['id'], menu['title'])
                dao.update_menu_structure(menu['id'], menu['structure'])
            elif 'active_menu' in request.POST:
                "Sets the selected menu as active"
                menu_id = jstree2mongo2(request.POST)['id']
                dao.update_active_menu(client_id, menu_id)
    else:
        #This case handles when request.method == GET
        #When the page is loaded the first time
        pass  
    return render(request, 'desktop_index.html',
                  {'menus': menus, 'items': simplejson.dumps(items),
                   'json_menus': mongo2jstree_list(menus),
                   'template': 'manager_menus.html',
                   'title': 'Manager'})


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

####################
# Helper functions #
####################

def mongo2jstree(menu):
    '''Changes the structure of the menu that uses mongo
    to a way jstree can read it'''
    #TODO: maybe use some recursion so the tree doesnt have a fixed depth <-- Done below
    tree = {'data': []}
    i = 0
    tree['data'].append({'data': menu['title'], 'attr': {'id': menu['_id'], 'rel': 'root'}, 'state': 'open', 'children': []})
    for section in menu['structure']:
        tree['data'][0]['children'].append({'data': section, 'attr': {'rel': 'section'},'state': 'open','children':[]})
        j = 0
        for subsection in menu['structure'][section]:
            tree['data'][0]['children'][i]['children'].append({'data': subsection, 'attr': {'rel': 'subsection'}, 'state': 'open','children':[]})
            for item in menu['structure'][section][subsection]:
                tree['data'][0]['children'][i]['children'][j]['children'].append({'data': dao.get_item(item)['name'], 'attr': {'id': item, 'rel': 'item'}})
            j += 1
        i += 1
    return simplejson.dumps(tree)

def mongo2jstree2(menu):
    '''Changes the structure of the menu that uses mongo
    to a way jstree can read it
    P.S: This function can go to infinite depth'''
    tree = {'data': []}
    i = 0
    tree['data'].append({'data': menu['title'], 'attr': {'id': str(menu['_id']), 'rel': 'root'}, 'state': 'open', 'children': []})
    explo(menu, tree = tree)
    return simplejson.dumps(tree)

def explo(data, name='', level = 0, path=[], tree = {'data': []}):
    if 'structure' in data:
        for child in data['structure']:
            explo(data['structure'][child], name=child, tree = tree)
    elif type(data) is dict:
        level += 1
        ##### SECTIONS #####
        path.insert(level-1, name)
        path = path[:level]
        eval(p2d(path, level)).insert(0, {'data': name, 'attr': {'rel': 'section'},'state': 'open','children':[]})

        for child in data:
            explo(data[child], name=child, level=level, path=path, tree=tree)
    elif type(data) is list:
        level += 1
        ##### SUBSECTIONS ######
        path.insert(level-1, name)
        path = path[:level]
        eval(p2d(path, level)).insert(0, {'data': name, 'attr': {'rel': 'subsection'}, 'state': 'open','children':[]})
       
        level += 1
        for child in data:
            ##### ITEMS #####
            eval(p2d(path, level)).insert(0, {'data': dao.get_item(child)['name'], 'attr': {'id': child, 'rel': 'item'}})


def p2d(path, level):
    string = "tree['data'][0]['children']"
    for branch in path[:level-1]:
        string += "[0]['children']"
    return string

def mongo2jstree_list(menus):
    '''handles multiple menus with the function above'''
    js_menus = []
    for menu in menus:
        js_menus.append(mongo2jstree2(menu))
    return js_menus                  

def jstree2mongo(tree):
    '''Changes the structure of the menu that uses jstree
    to the origal way that mongo uses'''
    #TODO: maybe use some recursion so it doesnt read the tree to a fixed depth <-- Done below
    #Waiting for cesar's approval to delete this function and keep the new one below :)
    body = simplejson.loads(tree['tree'])
    structure = {}
    for section in body[0]['children']:
        structure[section['data']] = {}
        if 'children' in section:
            for subsection in section['children']:
                structure[section['data']][subsection['data']] = []
                if 'children' in subsection:
                    for item in subsection['children']:
                        structure[section['data']][subsection['data']].append(item['attr']['id'])
    return {unicode('structure'): structure, unicode('title'): body[0]['data'], unicode('id'): body[0]['attr']['id']}
    
def jstree2mongo2(tree):
    '''Changes the structure of the menu that uses jstree
    to the original way that mongo uses.
    P.S: This function can go to infinite depth'''
    body = simplejson.loads(tree['tree'])
    structure = {}
    explore(body[0], structure = structure)
    return {unicode('structure'): structure, unicode('title'): body[0]['data'], unicode('id'): body[0]['attr']['id']}

def dictizeString(string, dictionary, item_id = unicode(), subsection = unicode(), section = unicode()):
    '''Help enters the path(string) in the structure(dictionary)''' 
    while string.startswith('/'):
        string = string[1:]
    parts = string.split('/', 1)
    if len(parts) > 1:
        branch = dictionary.setdefault(parts[0], {})
        dictizeString(parts[1], branch, item_id = item_id, subsection = subsection, section = section)
    else:
        if item_id:
            if dictionary.has_key(parts[0]):
                 dictionary[parts[0]].append(item_id)
            else:
                 dictionary[parts[0]] = [item_id]
        if subsection:
            if not dictionary.has_key(parts[0]):
                 dictionary[parts[0]] = []
        if section:
            if not dictionary.has_key(parts[0]):
                 dictionary[parts[0]] = {}

                                 
def explore(data, path = '', structure = {}):
    '''Explores de jstree with recursion'''
    if data['attr']['rel'] == 'root':
        if 'children' in data:
            for child in data['children']:
                explore(child, structure = structure)
            
    elif data['attr']['rel'] == 'section': 
        path += '/' + data['data']
        dictizeString(path, structure, section = data['data'])
        if 'children' in data:
            for child in data['children']:
                explore(child, path = path, structure = structure)
                
    elif data['attr']['rel'] == 'subsection':
        path += '/' + data['data']
        dictizeString(path, structure, subsection = data['data'])
        if 'children' in data:
            for child in data['children']:
                explore(child, path = path, structure = structure)
                
    elif data['attr']['rel'] == 'item':
        dictizeString(path, structure, item_id = data['attr']['id'])




