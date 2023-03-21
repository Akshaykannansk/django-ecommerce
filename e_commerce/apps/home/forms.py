from django import forms
from .models import *



class UpdateUserform(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"
            }
        ))
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','username', 'email', )

class profileform(forms.ModelForm):

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"

            }
        ))

    pincode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    country = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"

            }
        ))

    AboutMe = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"

            }
        ))

    class Meta:
        model = profile
        fields = ['address', 'city', 'pincode', 'country', 'AboutMe']


class ProductForm(forms.ModelForm):
    product_category = forms.ModelChoiceField(
        queryset=product_category.objects.all(), empty_label=None)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price',
                  'image', 'product_category', 'stock']
        widgets = {
            'image': forms.ClearableFileInput(),
            'category': forms.ModelChoiceField(queryset=product_category.objects.all())
        }


class productCategory(forms.ModelForm):

    category_name = forms.CharField(widget=forms.TextInput(
        attrs={

            "class": "form-control"
        }
    ))

    class Meta:
        model = product_category
        fields = ['category_name']
