# This module contains different methods to render a list of
# orders. In particular, we're interested in customers being able to
# view their orders in a different way than a server looks at
# orders. To do this, this module uses modifiers that 'implement the
# same interface' and then exposes a render_orders method that takes
# in a set of modifiers to be used.
import logging

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from orders.settings import dao

logger = logging.getLogger('orders')

# templates used by render_orders if no modifiers override them.
DEFAULT_TEMPLATES = {'top_template':'default_orders_header.html',
                     'item_template':'default_order_item.html'}

# MODIFIERS - all modifiers must implement this interface
# param: list of orders to be rendered.
# return: (dict, orders) where orders is the input list of orders
# updated by the modifier, and dict contains params to be passed to
# the template - including names for one or more template types. In
# particular, the following template types are currently supported:
# top_template, item_template and bottom_template
# TODO: Here are some other modifiers we might want to implement:
# sortable, filterable (by status, seat, time), timestamped,
# groupable. 
def verbose_item_decorator(orders):
    '''This decorator displays an order including the following
    information: item name, quantity, status, delay since order
    creation and cancel button if the order is cancelable
    (status==dao.ORDER_PLACED)'''
    for item in orders:
        if item['status'] == dao.ORDER_PLACED:
            item['cancelable'] = True
        item['status'] = item['status'].replace('_','').capitalize()
        if item['status'][-1] == 'g':
            item['delay'] = 'as of ' + item['delay']
    return {'item_template':'verbose_order.html'}, orders

def list_filter_decorator(orders):
    '''Displays a gear button on the right side of the header to allow
    the user to apply filters to the list of orders shown. Ideal for
    servers to filter by status, seat, time, etc'''
    return {'top_template':'order_list_filters.html'}, orders

def searchable_list_modifier(items):
    '''Enables a search filter on top of the list of orders. Useful
    for servers to filter by item name.'''
    return {'searchable':True}, items

def cancelable_item_modifier(items):
    '''This item modifier adds a cancel button on to the item if the
    item is still in ORDER_PLACED status.'''
    for item in items:
        if item['status'] == dao.ORDER_PLACED:
            item['cancelable'] = True
    return {'item_template':'cancelable_timestamped_item.html'},items

def bill_orders_modifier(items):
    ''' trivial modifier that adds a button to the bottom of the
    template to request the bill for the user's orders.'''
    return {'bottom_template':'bill_btn.html'}, items

# RENDERER
def render_orders(request, orders, modifiers=[]):
    '''Generic and flexible function that renders a list of orders
    according to the given set of modifiers using a strategy pattern
    (see http://en.wikipedia.org/wiki/Strategy_pattern). Each modifier
    takes the list of orders and outputs two objects: 1- a dict of
    params to be passed to the template - optionally including
    template types and names if the modifier uses them; 2- the list of
    orders to be passed to the template optionally with some
    attributes added or updated as needed by the template used by the
    modifier. The modifiers are executed in the order they appear in
    the input list. This function provides an extensible way to
    centralize the logic so that, for example, the difference between
    rendering orders for a customer or a server is just a matter of
    specifying a different set of modifiers if desired.  TODO:
    refactor list_orders in views.py to use this renderer and move the
    more flexible myorders.html to replace orders.html'''
    template_params = DEFAULT_TEMPLATES.copy()
    template_params['template'] = 'orders.html'
    client_id = request.session['client_id']
    client_name = dao.get_client_name(client_id)
    template_params['client_name'] = client_name
    template_orders = orders
    for mod in modifiers:
        params, template_orders = mod(template_orders)
        template_params.update(params)
    template_params['orders'] = template_orders
    logger.info({'template parameters':template_params})
    return render(request, 'index.html', template_params)
