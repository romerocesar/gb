# this module may contain over time several renderers for a
# menu. Ideally, views won't refer directly to renderers defined here
# by name, but will make use of dependency injection and the strategy
# pattern by configuring the desired renderers in orders/settings.py
import logging

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from orders.settings import dao

logger = logging.getLogger('orders')

def render_two_lvl_menu(request, menu={}, path=''):
    logger.debug('menu:%s, path:%s', menu, path)
    # parse input path and extract section if there is one
    levels = [section for section in path.split('/') if section.strip()]
    section = levels[1] if len(levels) == 2 else ''
    # section
    if section:
        division = levels[0]
        ids = menu['structure'][division][section]
        items = dao.get_items(ids)
        logger.info('items %s', items)
        return render(request, 'index.html',
                      {'template':'section.html', 'name':section, 'items':items})
    # top level
    else:
        return render(request, 'index.html',
                      {'menu':menu, 'template':'twolvlmenu.html', 'title':'Menu'})

def render_tree_menu(request, menu={}, path=''): 
    '''Renders the menu as a browsable tree. <path> indicates with
    section of <menu> to display items from. The resulting view will
    have at least one divider and the items within each divider. This
    function doesn't require the tree that defines the menu to be
    balanced, so each item being rendered could correspond to a menu
    item (a leaf node) or a section. If the path leads to leaf nodes,
    then these items are pulled from the db so their name can be
    displayed.'''
    logger.debug('menu:%s, path:%s',menu,path)
    sections = [section for section in path.split('/') if section.strip()]
    result = menu['structure']
    # go to the specified path within the menu
    for section in sections:
        result = result[section]
    # prepare items to be rendered
    template_items = []
    if type(result) == list:
        # there's no more subsections; we pull items from the DB to display them.
        template_items = dao.get_items(result)
        for item in template_items:
            item['type'] = 'item'
        # insert a divider so it's clear for the user.
        template_items.insert(0, {'type':'divider', 'name':sections[-1]})
    elif type(result) == dict:
        for divider in result:
            template_items.append({'type':'divider', 'name':divider})
            section = result[divider]
            for item in section:
                if type(section) == list:
                    # item is a leaf node (menu entry).
                    items = dao.get_items(section)
                    for x in items:
                        x['type'] = 'item'
                        template_items.append(x)
                    # break to move to the next divider 
                    break
                elif type(section) == dict:
                    # item is a subsection
                    template_items.append({'type':'section','name':item,
                                           'path':'/'.join((path, divider, item))})
    logger.info('items: %s', template_items)
    return render(request, 'index.html', {'items':template_items, 'menu_id': menu['id'],
                                          'template':'tree_menu.html', 'path':path})
