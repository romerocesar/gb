from django import forms
from settings import manager

class SectionForm(forms.Form):
    name = forms.CharField(max_length=50)
    inside = forms.CharField(max_length=50, required=False)
    has_subsections = forms.BooleanField(required=False)

class ItemForm(forms.Form):
    name = forms.CharField(max_length=50)
    price = forms.FloatField(min_value=0)

class ItemInsert(forms.Form):
    items = manager.get_items()
    it = [(i['_id'], i['name']) for i in items]
    choice = []
    for i in xrange(len(it)):
        choice.append((it[i][0], it[i][1]))
    insert = forms.ChoiceField(choices=choice)
    inside = forms.CharField(max_length=50)
