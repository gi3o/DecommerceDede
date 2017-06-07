from django import forms
from django.forms import ModelForm, Select, TextInput, Textarea, IntegerField, NumberInput, FileInput, ModelChoiceField
from .models import Product, ProductReview, Category, SellerProfile


class ProductReviewForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ['stars', 'title', 'review']
        widgets = {
            'stars': Select(attrs={'class':'w3-select w3-input w3-light-gray w3-border-0'}),
            'title': TextInput(attrs={'class':'w3-input w3-margin-bottom', 'placeholder':'Titolo'}),
            'review': Textarea(attrs={'class':'w3-input', 'placeholder':'Recensione'})
            }
"""
class ProductReviewForm(forms.Form):
    stars = forms.ChoiceField(choices= STAR_CHOICES, label= 'Stelle', widget= forms.Select(
                              attrs={'class':'w3-select w3-input w3-light-gray w3-border-0'}))
    title = forms.CharField(max_length= 30, widget= forms.TextInput(
                                attrs= {'class':'w3-input w3-margin-bottom', 'placeholder':'Titolo'}))
    review = forms.CharField(max_length= 280, widget= forms.Textarea(
                                 attrs= {'class':'w3-input', 'placeholder':'Review'}))"""

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
                               widget=forms.PasswordInput(
                                   attrs={'class':'w3-input w3-margin-bottom w3-third', 'placeholder':'Password'}))
    type = forms.ChoiceField(label='Tipo', choices=REGISTER_CHOICES, widget=forms.Select(
                                attrs={'class':'w3-select w3-input w3-margin-bottom w3-third'}))
    nationality = forms.ChoiceField(label='Nazionalità', choices=NATION_CHOICES, widget=forms.Select(
                                    attrs={'class':'w3-select w3-input w3-margin-bottom w3-third'}),
                                    required= False)
    address = forms.CharField(max_length = 60, label='Indirizzo', widget= forms.TextInput(
                                attrs={'class':'w3-select w3-input w3-margin-bottom w3-third', 'placeholder':'Indirizzo'}),
                                required = False)
    store_name = forms.CharField(max_length=40, label = 'Nome negozio', widget = forms.TextInput(
                                 attrs ={'class':'w3-input w3-margin-bottom w3-third', 'placeholder':'Nome negozio'}),
                                 required= False)

class UploadProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'details', 'price', 'image', 'stock']
        widgets = {
            'name':TextInput(attrs={'class':'w3-input', 'placeholder':'Nome Prodotto'}),
            'category': Select(choices = Category.objects.all(), attrs={'class':'w3-select w3-input'}),
            'details': Textarea(attrs={'class':'w3-input', 'placeholder':'Dettagli'}),
            'price': NumberInput(attrs={'class':'w3-input'}),
            'stock': NumberInput(attrs={'class':'w3-input'}),
            'image': FileInput(),
            }

class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class':'w3-input', 'placeholder':'Nome Categoria'}),
        }


