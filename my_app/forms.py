
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product , ProductAttribute


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name','isbn', 'quantity', 'purchasing_price', 'sale_price', 'supplier',
             'publisher', 'production_date', 'category', 'author'#, 'expiry_date'
        ]
        labels = {
            'product_name': _('Product Name'),
            'isbn': _('ISBN'),
            'quantity': _('Quantity'),
            'purchasing_price': _('Purchasing Price'),
            'sale_price': _('Sale Price'),
            'supplier': _('Supplier'),
            'publisher': _('Publisher'),
            'production_date': _('Production Date'),
            'category': _('Category'),
            'author': _('Author'),
            'expiry_date': _('Expiry Date'),
        }
        widgets = {
            'production_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }



class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ('attribute_name', 'value_type', 'attribute_value')
        labels = {
            'attribute_name': _('Attribute Name'),
            'value_type': _('Value Type'),
            'attribute_value': _('Attribute Value'),
        }
        help_texts = {
            'attribute_name': _('Enter the attribute name.'),
            'value_type': _('Select the value type.'),
            'attribute_value': _('Enter the value for this attribute.'),
        }

ProductAttributeFormSet = forms.inlineformset_factory(
    Product,
    ProductAttribute,
    form=ProductAttributeForm,
    fields=('attribute_name', 'value_type', 'attribute_value'),
    extra=1,
    can_delete=True
)


# class ProductAttributeForm(forms.ModelForm):
#     class Meta:
#         model = ProductAttribute
#         fields = ['attribute_name', 'value_type', 'attribute_value_text', 'attribute_value_number', 'attribute_value_date']

#     def clean(self):
#         cleaned_data = super().clean()
#         value_type = cleaned_data.get('value_type')

#         # التأكد من أن الحقل المناسب غير فارغ
#         if value_type == 'text' and not cleaned_data.get('attribute_value_text'):
#             raise forms.ValidationError("يرجى إدخال قيمة نصية.")
#         if value_type == 'number' and cleaned_data.get('attribute_value_number') is None:
#             raise forms.ValidationError("يرجى إدخال قيمة رقمية.")
#         if value_type == 'date' and not cleaned_data.get('attribute_value_date'):
#             raise forms.ValidationError("يرجى إدخال تاريخ.")
#         return cleaned_data

# from .models import Employee

# class EmployeeForm(forms.ModelForm):
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
#         label="Confirm Password"
#     )

#     class Meta:
#         model = Employee
#         fields = [
#             'first_name',
#             'last_name',
#             'email',
#             'DOB',
#             'password',
#             'confirm_password',
#             'manager',
#             'is_active',
#         ]
#         widgets = {
#             'DOB': forms.DateInput(attrs={'type': 'date'}),
#             'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password and confirm_password and password != confirm_password:
#             self.add_error('confirm_password', "Passwords do not match.")
#         return cleaned_data
