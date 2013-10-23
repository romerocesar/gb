clients = [
    {'_id':'c0',
     'menu':'m0',
     'menus': ['m0', 'm1'], 
     'seats':['s0', 's1','s2','s3'],
     'name':'Foo'
    }
]

menus = [
    {'_id':'m0',
     'title': 'My main bootstrapped menu',
     'structure': {
         'Food':{
             'Appetizers':['0','1','2','3'],
             'Main Dishes':['4','5','6','7','8','9'],
             'Desserts':['10','11'],
         },
         'Drinks': {
             'Sodas':[],
             'Juices':[],
             'Wines':[],
             'Beers':[],
             'Cocktails':[]
         }
     }
    },
    {'_id': 'm1',
     'title': 'Other menu',
     'structure': {
         'Drinks': []
         }
     },
    {'_id': 'm2',
     'title': 'Menu title',
     'structure': {
         'Food': []
         }
     }
]

items = [
    {'_id':'0','client_id':'c0', 'name':'sweet potato fries', 'description':'served with brown sugar cream cheese and housemade barbecue sauce', 'price':6.99},
    {'_id':'1','client_id':'c0', 'name':'tapas with flatbread', 'description':'flatbread served with bruschetta, hummus and olive tapenade.', 'price':6.99},
    {'_id':'2','client_id':'c0', 'name':'sweet chili chicken wings', 'description':'with a housemade sweet chili glaze', 'price':7.99},
    {'_id':'3','client_id':'c0', 'name':'kobe sliders', 'description':'three premium american kobe mini-burgers served on housemade rolls', 'price':8.99},
    {'_id':'4','client_id':'c0', 'name':'bourbon salmon', 'description':'grilled salmon brushed with woodford reserve bourbon. Seasonal vegetables on the side', 'price':16.99},
    {'_id':'5','client_id':'c0', 'name':'korean bbq pork chop', 'description':'korean soy-cili glaze, marinated shiitake mushrooms and soy butter sauce', 'price':14.99},
    {'_id':'6','client_id':'c0', 'name':'flame grilled new york strip', 'description':'perfectly trimmed short loin, selected by our butcher for tenderness and light marble', 'price':17.99},
    {'_id':'7','client_id':'c0', 'name':'cajun fish taco', 'description':'a spicy pescadorian twist on the traditional baja taco. Four servings.', 'price':14.99},
    {'_id':'8','client_id':'c0', 'name':'Tuscan chicken pasta', 'description':'grilled chicken tossed with tomatoes and fresh basil over linguine.', 'price':15.99},
    {'_id':'9','client_id':'c0', 'name':'lobster and jumbo lump crab cake', 'description':'blended jumbo lump crab and maine lobster with apple cider coleslaw, garlic fries and our signature tartar sauce', 'price':17.99},
    {'_id':'10','client_id':'c0', 'name':'warm apple bread pudding', 'description':"with pecans, vanilla ice cream and whiskey sauce", 'price':6.99},
    {'_id':'11','client_id':'c0', 'name':'Ultimate double chocolate cake', 'description':"chocolate cake layered with chocolate mousse and housemade fudge", 'price':6.99}
]
