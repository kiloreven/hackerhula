from django import forms


class PayForm(forms.Form):
    amountt = forms.CharField(label='amountt', max_length=100)
    stripeToken = forms.CharField(label='stripeToken', max_length=100)


