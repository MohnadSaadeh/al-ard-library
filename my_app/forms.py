
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product , ProductAttribute
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name','isbn', 
            # 'quantity', 
            # 'purchasing_price', 
            'sale_price', 
            # 'supplier',
             'publisher', 
             'production_date', 
             'category', 
             'author'
             #, 'expiry_date'
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('product_name', css_class='col-md-4 mb-3'),
                Column('isbn', css_class='col-md-4 mb-3'),
                Column('sale_price', css_class='col-md-4 mb-3'),
            ),
            Row(
                Column('publisher', css_class='col-md-4 mb-3'),
                Column('production_date', css_class='col-md-4 mb-3'),
                Column('category', css_class='col-md-4 mb-3'),
            ),
            Row(
                Column('author', css_class='col-md-4 mb-3'),
            ),
        )



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
