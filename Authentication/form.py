from django import forms


"""
    These forms take the data passed from the html file and check them again by
    adding more constarints, then storing the received values in their attributes
    by creating instances of their classes
"""


class Register (forms.Form):
    
    Username = forms.CharField(required=True, min_length=6)
    email = forms.EmailField(required=True )
    age = forms.IntegerField(min_value=16, max_value=100, required=True)
    password = forms.CharField(min_length=6, required=True)
    phoneNo = forms.CharField(min_length=11, max_length=11,  required=True)


class Login (forms.Form):
    Username = forms.CharField(required=True , min_length=2)
    password = forms.CharField(min_length=6, required=True)


