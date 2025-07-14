from django import forms
from .models import Category,Products

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ['created_at']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Price can't be negative.") 
        return price

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name[0].isupper():
            raise forms.ValidationError("product name must start with capital letter.")
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        if name.lower() == description.lower():
                raise forms.ValidationError("Product name and description can't be same.")
        return cleaned_data
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')
        if name.lower() == category.lower():
                raise forms.ValidationError("Product name and category name can't be same.")
        return cleaned_data


