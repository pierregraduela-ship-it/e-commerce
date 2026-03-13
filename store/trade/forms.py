from django import forms
from .models import Order,Product,Category,Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name','email', 'address', 'city', 'phone']


        # Formulaire produit
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'image']



        #securite#

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")

        return email



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

        

        #category#

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
