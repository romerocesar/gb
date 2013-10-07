class OrdersDAO:
    # order statii
    ORDER_PLACED = '_placed_'
    ORDER_PREPARED = '_prepared_'
    ORDER_SERVED = '_served_'
    BILL_REQUESTED = '_bill requested_'
    ORDER_BILLED = '_billed_'
    ORDER_PAID = '_paid_'
    ORDER_RETURNED = '_returned_'
    ORDER_CANCELED = '_canceled_'

    ORDER_STATII = (ORDER_PLACED, ORDER_RETURNED, ORDER_PAID, ORDER_SERVED, ORDER_PREPARED, BILL_REQUESTED, ORDER_BILLED)
