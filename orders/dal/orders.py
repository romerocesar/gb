class OrdersDAO:
    # order statii
    ORDER_PLACED = '_placed_'
    ORDER_CANCELED = '_canceled_'
    ORDER_PREPARING = '_preparing_'
    ORDER_PREPARED = '_prepared_'
    ORDER_SERVED = '_served_'
    BILL_REQUESTED = '_bill requested_'
    ORDER_BILLED = '_billed_'
    ORDER_PAID = '_paid_'
    ORDER_RETURNED = '_returned_'

    ORDER_STATII = (ORDER_PLACED,
                    ORDER_CANCELED,
                    ORDER_PREPARING,
                    ORDER_PREPARED,
                    ORDER_SERVED,
                    ORDER_RETURNED,
                    BILL_REQUESTED,
                    ORDER_BILLED,
                    ORDER_PAID)
