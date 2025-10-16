from django.db import models 
import datetime 
from django.utils import timezone 
import re 
from django.utils.translation import gettext as _

# from . import views

class EmployeeManager(models.Manager):
    def employee_validator(self, postData):
        dob_val = datetime.date.today()
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['f_name']) < 2:
            errors['f_name'] = _("First name should be at least 2 characters")
        if len(postData['l_name']) < 2:
            errors['l_name'] = _("Last name should be at least 2 characters")
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = _("Invalid email address!")
        if postData['DOB'] == "":
            errors['DOB'] = _("Please enter a date")
        if postData['DOB'] and datetime.datetime.strptime(postData['DOB'], '%Y-%m-%d').date() >= dob_val:
            errors['DOB'] = _("Date should be in the past")
        if len(postData['password']) < 8:
            errors['password'] = _("Password should be at least 8 characters")
        if postData['password'] != postData['c_password']:
            errors['c_password'] = _("Passwords do not match")
        return errors
    
    def login_employee_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = _("Invalid email address!")
        if len(postData['password']) < 8:
            errors['c_password'] = _("Password should be at least 8 characters")
        return errors

class ManagerManager(models.Manager):
    def manager_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['admin_first_name']) < 2:
            errors['admin_first_name'] = _("First name should be at least 2 characters")
        if len(postData['admin_last_name']) < 2:
            errors['admin_last_name'] = _("Last name should be at least 2 characters")
        if not EMAIL_REGEX.match(postData['admin_email']):
            errors['admin_email'] = _("Invalid email address!")
        if len(postData['admin_phone']) < 10:
            errors['admin_phone'] = _("Phone number should be at least 10 characters")
        if len(postData['admin_password']) < 8:
            errors['admin_password'] = _("Password should be at least 8 characters")
        if postData['admin_repete_password'] != postData['admin_password']:
            errors['admin_repete_password'] = _("Passwords do not match")
        return errors
    
    def login_manager_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = _("Invalid email address!")
        if len(postData['password']) < 8:
            errors['password'] = _("Password should be at least 8 characters")
        return errors

class ProductManager(models.Manager):
    def product_validator(self, postData):
        errors = {}
        if len(postData['product_name']) < 2:
            errors['product_name'] = _("Product name should be at least 2 characters")
        if postData['quantity'] == "":
            errors['quantity'] = _("Please enter a quantity")
        # if postData['quantity'] < 0:
        #     errors['quantity'] = _("Insufficient stock")
        if postData['purchasing_price'] == "":
            errors['purchasing_price'] = _("Please enter a purchasing price")
        if postData['product_name'] == "":
            errors['product_name'] = _("Please enter a product name")
        # if postData['expiry_date'] == "":
        #     errors['expiry_date'] = _("Please enter an expiry date")
        # if postData['expiry_date'] < str(datetime.date.today()):
        #     errors['expiry_date'] = _("Expiry date should be in the future")
        if postData['supplier'] == "":
            errors['supplier'] = _("Please enter a supplier")
        return errors

class PurchaseManager(models.Manager):
    def invoice_validator(self, postData):
        errors = {}
        if (postData['product_name']) == "- Select Product -":
            errors['product_name'] = _("Choose a Product Please")
        if (postData['quantity'] == "") or (postData['quantity'] == "0" ):
            errors['quantity'] = _("Please enter a quantity")
        # if postData['supplier'] == "":
        #     errors['supplier'] = "Please enter a supplier"
        return errors

from django.db import models

class Sale_orderManager(models.Manager):
    def invoice_sale_validator(self, postData):
        # Import here to avoid circular import
        from .models import Product  

        product = Product.objects.filter(product_name=postData.get('product_name')).first()
        errors = {}

        if not product:
            errors['product_name'] = _("⚠️ Product not found.")
            return errors

        try:
            quantity = int(postData.get('quantity', 0))
        except ValueError:
            errors['quantity'] = _("⚠️ Quantity must be a number.")
            return errors

        if quantity <= 0:
            errors['quantity'] = _("⚠️ Quantity must be greater than zero.")
        elif product.quantity == 0:
            errors['quantity'] = _("⚠️ Out of stock.")
        elif product.quantity < quantity:
            errors['quantity'] = _(f"⚠️ Only {product.quantity} left in stock.")

        return errors





