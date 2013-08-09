from django.http import HttpResponse
from django.shortcuts import render

from settings import dao

from orders.forms import SectionForm, ItemForm, ItemInsert

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

def dish(request, dish_id):
    dish = dao.get_dish(dish_id)
    return render(request, 'index.html',
                 {'template':'dish.html', 'title':dish['name'], 'dish':dish})

def section(request, menu_id, division, section):
    print('section',menu_id,section)
    menu = dao.get_menu(menu_id)
    ids = menu['structure'][division][section]
    items = dao.get_items(ids)
    print('items ', items)
    return render(request, 'index.html',
                {'template':'section.html', 'name':section, 'items':items})

def managerview(request, client_id):
    #TODO: some refactoring,
    #      make the form validations work with the javascript part
    menu = dao.m_get_menu(client_id)
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

