from django import forms


class SectionForm(forms.Form):
    name = forms.CharField(max_length=50)
    inside = forms.CharField(max_length=50, required=False)
    has_subsections = forms.BooleanField(required=False)

class ItemForm(forms.Form):
    name = forms.CharField(max_length=50)
    price = forms.FloatField(min_value=0, initial=0)
    description = forms.CharField(max_length=200, widget=forms.Textarea, initial="Description of the item")

def get_my_choices(items):
    choice = [(i['_id'], i['name']) for i in items]
    return choice

class ItemInsert(forms.Form):

    def __init__(self, *args, **kwargs):
        choice = kwargs.pop('choices', None)
        super(ItemInsert, self).__init__(*args, **kwargs)
        self.fields['insert'] = forms.ChoiceField(
            choices=get_my_choices(choice), label='Item' )
        self.fields['inside'] = forms.CharField(max_length=50)
   
