from django import forms


class SectionForm(forms.Form):
    name = forms.CharField(max_length=50)
    inside = forms.CharField(max_length=50, required=False)
    has_subsections = forms.BooleanField(required=False)

class ItemForm(forms.Form):
    name = forms.CharField(max_length=50)
    price = forms.FloatField(min_value=0)

def get_my_choices(items):
    it = [(i['_id'], i['name']) for i in items]
    choice = []
    for i in xrange(len(it)):
        choice.append((it[i][0], it[i][1]))
    return choice

class ItemInsert(forms.Form):

    def __init__(self, *args, **kwargs):
        choice = kwargs.pop('choices', [])
        super(ItemInsert, self).__init__(*args, **kwargs)
        self.fields['insert'] = forms.ChoiceField(
            choices=get_my_choices(choice) )
        self.fields['inside'] = forms.CharField(max_length=50)
    """
    items = []
    it = [(i['_id'], i['name']) for i in items]
    choice = []
    for i in xrange(len(it)):
        choice.append((it[i][0], it[i][1]))
    insert = forms.ChoiceField(choices=choice)
    """
    #inside = forms.CharField(max_length=50)
