from django import forms


class BasicForm(forms.Form):
    salary = forms.DecimalField()
    status = forms.CharField()
    user = forms.IntegerField()