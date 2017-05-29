from django import forms


CHOICES=[(1, '1'),
         (2, '2'),
         (3, '3'),
         (4, '4'),
         (5, '5')]

class ProductReviewForm(forms.Form):
    stars = forms.ChoiceField(choices= CHOICES, label= 'Stelle', widget= forms.Select(
                              attrs={'class':'w3-select, w3-input w3-light-gray w3-border-0'}))
    title = forms.CharField(max_length= 30, widget= forms.TextInput(
                                attrs= {'class':'w3-input w3-margin-bottom', 'placeholder':'Titolo'}))
    review = forms.CharField(max_length= 280, widget= forms.Textarea(
                                 attrs= {'class':'w3-input', 'placeholder':'Review'}))

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username', widget= forms.TextInput(
                                attrs={'class':'w3-input w3-margin-bottom', 'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput())