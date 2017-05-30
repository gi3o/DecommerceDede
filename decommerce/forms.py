from django import forms
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, \
    CommonPasswordValidator, NumericPasswordValidator

STAR_CHOICES=[(1, '1'),
         (2, '2'),
         (3, '3'),
         (4, '4'),
         (5, '5')]


class ProductReviewForm(forms.Form):
    stars = forms.ChoiceField(choices= STAR_CHOICES, label= 'Stelle', widget= forms.Select(
                              attrs={'class':'w3-select w3-input w3-light-gray w3-border-0'}))
    title = forms.CharField(max_length= 30, widget= forms.TextInput(
                                attrs= {'class':'w3-input w3-margin-bottom', 'placeholder':'Titolo'}))
    review = forms.CharField(max_length= 280, widget= forms.Textarea(
                                 attrs= {'class':'w3-input', 'placeholder':'Review'}))

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username', widget= forms.TextInput(
                                attrs={'class':'w3-input w3-margin-bottom w3-third', 'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'w3-input w3-margin-bottom w3-third'}))

REGISTER_CHOICES = [('Compratore','Compratore'), ('Venditore','Venditore')]
NATION_CHOICES = [('ITA', 'Italia'),
                  ('ENG', 'Ingilterra'),
                  ('USA', 'Stati Uniti'),
                  ('FRA', 'Francia'),
                  ('SPA', 'Spagna')]

class RegisterForm(forms.Form):
    mail = forms.EmailField(label='E-mail', widget= forms.TextInput(
                            attrs={'class':'w3-input w3-margin-bottom w3-third', 'placeholder':'E-mail'}))
    username = forms.CharField(max_length=30, label = 'Username', widget= forms.TextInput(
                                attrs={'class':'w3-input w3-margin-bottom w3-third', 'placeholder':'Username'}))
    password = forms.CharField(label = 'Password',
                               validators= [MinimumLengthValidator(), UserAttributeSimilarityValidator(),
                                            CommonPasswordValidator(), NumericPasswordValidator()],
                               widget=forms.PasswordInput(
                                   attrs={'class':'w3-input w3-margin-bottom w3-third', 'placeholder':'Password'}))
    type = forms.ChoiceField(label='Tipo', choices=REGISTER_CHOICES, widget=forms.Select(
                                attrs={'class':'w3-select w3-input w3-margin-bottom w3-third'}))
    nationality = forms.ChoiceField(label='Nazionalità', choices=NATION_CHOICES, widget=forms.Select(
                                    attrs={'class':'w3-select w3-input w3-margin-bottom w3-third'}))
    address = forms.ChoiceField(label='Indirizzo', widget= forms.Select(
                                attrs={'class':'w3-select w3-input w3-margin-bottom w3-third'}))
    store_name = forms.CharField(max_length=40)


