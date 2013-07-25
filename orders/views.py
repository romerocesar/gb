from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader

from settings import dao

def menu(request, client_id):
    try:
        client_id = int(client_id)
        menu = dao.get_menu(client_id)
    except ValueError:
        print('invalid client id '+client_id)
        menu = dao.get_menu()
    return render(request, 'menu.html', {'menu':menu})
