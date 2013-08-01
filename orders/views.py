from django.http import HttpResponse
from django.shortcuts import render

from settings import dao
from dal.mongo import ManagerDAO

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

def managerview(request, client_name):
    manager = ManagerDAO(client_name)
    menu = manager.get_menu()
    items = manager.get_items()
    if request.method == 'POST':
        if 'add_section' in request.POST:
            section_form = SectionForm(request.POST)
            item_form = ItemForm()
            iteminsert_form = ItemInsert(choices=items)
            if section_form.is_valid():
                cd = section_form.cleaned_data
                name = cd['name']
                has_subsections = cd['has_subsections']
                inside = cd['inside']
                manager.add_section(name, has_subsections, inside)
        elif 'delete_section' in request.POST:
            section_form = SectionForm(request.POST)
            item_form = ItemForm()
            iteminsert_form = ItemInsert(choices=items)
            if section_form.is_valid():
                cd = section_form.cleaned_data
                name = cd['name']
                inside = cd['inside']
                manager.del_section(name, inside)
        elif 'add_item' in request.POST:
            section_form = SectionForm()
            item_form = ItemForm(request.POST)
            iteminsert_form = ItemInsert(choices=items)
            if item_form.is_valid():
                cd = item_form.cleaned_data
                name = cd['name']
                price = cd['price']
                manager.add_item(name, price)
        elif 'delete_item' in request.POST:
            section_form = SectionForm()
            item_form = ItemForm(request.POST)
            iteminsert_form = ItemInsert(choices=items)
            if item_form.is_valid():
                cd = item_form.cleaned_data
                name = cd['name']
                price = cd['price']
                manager.del_item(name)
        elif 'insertitem' in request.POST:
            section_form = SectionForm()
            item_form = ItemForm()
            iteminsert_form = ItemInsert(request.POST, choices=items)
            if iteminsert_form.is_valid():
                cd = iteminsert_form.cleaned_data
                insert = cd['insert']
                inside = cd['inside']
                manager.insert_item(insert, inside)
        elif 'remove_from' in request.POST:
            section_form = SectionForm()
            item_form = ItemForm()
            iteminsert_form = ItemInsert(request.POST, choices=items)
            if iteminsert_form.is_valid():
                cd = iteminsert_form.cleaned_data
                insert = cd['insert']
                inside = cd['inside']
                manager.remove_item_from(insert, inside)
    else:
        section_form = SectionForm()
        item_form = ItemForm()
        iteminsert_form = ItemInsert(choices=items)
    return render(request, 'manager.html',
                  {'menu': menu, 'items': items,
                   'section_form': section_form,
                   'item_form': item_form,
                   'iteminsert': iteminsert_form})

