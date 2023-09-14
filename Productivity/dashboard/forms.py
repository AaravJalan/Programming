from email.policy import default
from django import forms

class NewTaskForm(forms.Form):
    name = forms.CharField(widget = forms.TextInput(attrs = {"placeholder": "Name", "class": "form-control", "style":"margin: 10px 0 5px 0"}))
    action = forms.CharField(required = False, widget = forms.Textarea(attrs = {"class": "form-control", "placeholder":"Information", "style":"margin-bottom:10px"}))

class AlarmForm(forms.Form):
    name = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'Alarm Name', 'class': 'alert alert-warning form-control mt-2 mb-2'}))
    date = forms.DateTimeField(
        input_formats = ['%d/%m/%Y %H:%M'],
        widget = forms.DateTimeInput(attrs = {
            'class': 'form-control alert alert-primary datetimepicker-input',
            'data-target': '#datetimepicker1',
        })
    )

class NewLinkForm(forms.Form):
    name = forms.CharField(widget = forms.TextInput(attrs = {"placeholder": "Name", "class": "form-control", "style":"margin: 10px 0 5px 0"}))
    link = forms.URLField(widget = forms.URLInput(attrs = {"placeholder": "Link", "class": "form-control", "style":"margin-bottom:5px"}))
    image = forms.URLField(widget = forms.URLInput(attrs = {"placeholder": "Image Link", "class": "form-control", "style":"margin-bottom:10px"}))