from django.db import models 
import datetime 
from django.utils import timezone 
import re 
# from . import views

class EmployeeManager(models.Manager):
    def employee_validator(self, postData):
        # dob_val = views.get_date_time()
        dob_val = datetime.date.today()
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First name should be at least 2 characters"
        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if postData['DOB'] == "":
            errors['DOB'] = "Please enter a date"
        
        if postData['DOB'] > str(dob_val):
            errors['DOB'] = "Date should be in the past"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['c_password'] != postData['password']:
            errors['c_password'] = "Passwords not match"
        return errors
    
    def login_employee_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['c_password'] = "Password should be at least 8 characters"
        return errors

class ManagerManager(models.Manager):
    def manager_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['admin_first_name']) < 2:
            errors['admin_first_name'] = "First name should be at least 2 characters"
        if len(postData['admin_last_name']) < 2:
            errors['admin_last_name'] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['admin_email']):
            errors['admin_email'] = "Invalid email address!"
        if len(postData['admin_phone']) < 10:
            errors['admin_phone'] = "Phone number should be at least 10 characters"
        if len(postData['admin_password']) < 8:
            errors['admin_password'] = "Password should be at least 8 characters"
        if postData['admin_repete_password'] != postData['admin_password']:
            errors['admin_repete_password'] = "Passwords do not match"
        return errors
    
    def login_manager_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        return errors

class ProductManager(models.Manager):
    def product_validator(self, postData):
        errors = {}
        if len(postData['product_name']) < 2:
            errors['product_name'] = "Product name should be at least 2 characters"
        if postData['quantity'] == "":
            errors['quantity'] = "Please enter a quantity"
        # if postData['quantity'] < 0:
        #     errors['quantity'] = "Insufficient stock"
        if postData['purchasing_price'] == "":
            errors['purchasing_price'] = "Please enter a purchasing price"
        if postData['product_name'] == "":
            errors['product_name'] = "Please enter a product name"
        # if postData['expiry_date'] == "":
        #     errors['expiry_date'] = "Please enter an expiry date"
        # if postData['expiry_date'] < str(datetime.date.today()):
        #     errors['expiry_date'] = "Expiry date should be in the future"
        if postData['supplier'] == "":
            errors['supplier'] = "Please enter a supplier"
        return errors

class PurchaseManager(models.Manager):
    def invoice_validator(self, postData):
        errors = {}
        if (postData['product_name']) == "- Select Product -":
            errors['product_name'] = "Choose a Product Please"
        if (postData['quantity'] == "") or (postData['quantity'] == "0" ):
            errors['quantity'] = "Please enter a quantity"
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
            errors['product_name'] = "⚠️ Product not found."
            return errors

        try:
            quantity = int(postData.get('quantity', 0))
        except ValueError:
            errors['quantity'] = "⚠️ Quantity must be a number."
            return errors

        if quantity <= 0:
            errors['quantity'] = "⚠️ Quantity must be greater than zero."
        elif product.quantity == 0:
            errors['quantity'] = "⚠️ Out of stock."
        elif product.quantity < quantity:
            errors['quantity'] = f"⚠️ Only {product.quantity} left in stock."

        return errors





