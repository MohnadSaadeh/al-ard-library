from django import forms
from .models import Product , ProductAttribute


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'quantity', 'purchasing_price', 'expiry_date', 'supplier']


ProductAttributeFormSet = forms.inlineformset_factory(
    Product,
    ProductAttribute,
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