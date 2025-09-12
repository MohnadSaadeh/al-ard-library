from django.db import models
from django.db.models import F, ExpressionWrapper, FloatField ,DecimalField, IntegerField
import re
from datetime import datetime , timedelta
import datetime
from .validations import EmployeeManager , ManagerManager , ProductManager , Purchasing_invoiceManager , Sale_orderManager


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20 , null=True )
    email = models.EmailField(max_length=255, null=True )
    contact_info = models.TextField(null=True) # address, notes, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=255 , null=True)
    contact_info = models.TextField() # address, notes, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# class ProductAttribute(models.Model):
#     attribute_name = models.CharField(max_length=255)
#     attribute_value = models.CharField(max_length=255)
#     product = models.ForeignKey('Product', related_name='attributes', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.product.product_name }{self.attribute_name}: {self.attribute_value}"

#--------------------------------------------------------------------MANAGER-----------------------


# Create your models here.
# the manager teble
# manager can add many imployees
class Manager(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.IntegerField()
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ManagerManager()
    # employees

def get_manager(id):#--------------------------------------------Mai
    return Manager.objects.get(id=id)
    
#--------------------------------------------------------------------EMPLOYEE-----------------------


# EMP adds many Products
# EMP can make many purchasing invoices
# EMP can make many sales orders
class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    DOB = models.DateField()
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    manager = models.ForeignKey(Manager , related_name="employees", on_delete=models.CASCADE) 
    is_active = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EmployeeManager()
    # products
    # purchasing_invoice
    # sale_orders

def add_employee(f_name, l_name, email, DOB, password, confirm_password ,manager_id ):
    manager = Manager.objects.get(id=manager_id)
    Employee.objects.create(first_name=f_name, last_name=l_name, email=email, DOB=DOB, password=password, confirm_password=confirm_password , manager = manager )
def get_all_employees():
    return Employee.objects.all()

def get_employee_by_id(id):
    return Employee.objects.get(id=id)






#--------------------------------------------------------------------PRODUCT-----------------------


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField() #stock_quantity
    purchasing_price = models.DecimalField(max_digits=6, decimal_places=2) # 999999.99
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, null=True , blank=True) # 999999.99
    category = models.CharField(max_length=100, blank=True, null=True)
    expiry_date  = models.DateField()
    supplier = models.CharField(max_length=255)  # Supplier NAME

    employee = models.ForeignKey(Employee , related_name="products", on_delete=models.CASCADE , null=True, blank=True) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()
    # purchasing_invoices
    # sale_orders
    # attributes
    def __str__(self):
        return self.product_name , self.employee.first_name
        
class ProductAttribute(models.Model):
    VALUE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    attribute_name = models.CharField(max_length=100)
    value_type = models.CharField(max_length=10, choices=VALUE_TYPE_CHOICES, default='text')
    attribute_value = models.CharField(max_length=255)

    def get_typed_value(self):
        """إرجاع القيمة بالنوع المناسب"""
        if self.value_type == 'number':
            try:
                return float(self.attribute_value)
            except ValueError:
                return None
        elif self.value_type == 'date':
            from datetime import datetime
            try:
                return datetime.strptime(self.attribute_value, "%Y-%m-%d").date()
            except ValueError:
                return None
        return self.attribute_value  # نص عادي

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"






def get_all_products():
    return Product.objects.all()

def get_product_expired():
    return Product.objects.filter(expiry_date__lt=datetime.date.today())

def delete_clicked_product(request):
    product=Product.objects.get(id=request.POST['product_id'])
    return product.delete()

def get_product(id):#--------------------------------------------Mai
    return Product.objects.get(id=id)

def update_selected_product(request,id):

    product=Product.objects.get(id=id)
    product.product_name=request.POST['product_name']
    product.quantity=request.POST['quantity']
    product.purchasing_price=request.POST['purchasing_price']
    product.expiry_date=request.POST['expiry_date']
    product.supplier=request.POST['supplier']
    product.employee=Employee.objects.get(id=request.session['employee_id'])

    product.save()

def out_of_stock():
    return Product.objects.filter(quantity=0)

def count_out_stock():
    return Product.objects.filter(quantity=0).count()#--------------------------------------------Mai


#--------------- not used -------------------
def get_six_monthes():
    today = datetime.date.today()
    six_months_later = today + timedelta(days=6*30)  # Assuming 30 days per month
    return Product.objects.filter(expiry_date__range=[today, six_months_later]).order_by('expiry_date')
#--------------- not used -------------------

def add_product(product_name, quantity, purchasing_price, expiry_date, supplier, employee_id):
    employee = Employee.objects.get(id=employee_id)
    Product.objects.create(product_name=product_name, quantity=quantity, purchasing_price=purchasing_price, expiry_date=expiry_date, supplier=supplier, employee = employee)
# this function return the products and 
# the total cost of each product 
# (purchasing_price * quantity)
# by adding a new field called total_cost
# with the Product.objects.annotate
def get_six_monthes_products():
    today = datetime.date.today()
    six_months_later = today + timedelta(days=6*30)
    products_with_total_cost = Product.objects.annotate(
        total_cost=F('purchasing_price') * F('quantity')
        ).order_by('expiry_date').filter(expiry_date__range=[today, six_months_later])
    return products_with_total_cost



    # البحث عن كل المنتجات التي لها تاريخ انتهاء صلاحية قبل 2025-01-01
    # expired_products = Product.objects.filter( 
    #     attributes__attribute_name="expiry_date",
    #     attributes__attribute_value__lt="2025-01-01"
    #     )

#--------------------------------------------------------------------PUECHASING-----------------------


# P.Inv contains many products
# P.Inv is made by one EMP
class Purchasing_invoice(models.Model):

    # product_name = models.CharField(max_length=255)
    # quantity = models.IntegerField()

    employee = models.ForeignKey(Employee , related_name="purchasing_invoices", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    products = models.ManyToManyField(Product, related_name="purchasing_invoices")
    # supplier = models.foreignKey(Supplier , related_name="purchasing_invoices", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Purchasing_invoiceManager()
    # products
    # purchase_items

# the P.Item table to link the invoice with the product and the quantity of each product in the invoice
class Purchase_item(models.Model):
    purchasing_invoice = models.ForeignKey(Purchasing_invoice, related_name="purchase_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="purchase_items", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
def get_all_invoices():
    return Purchasing_invoice.objects.all().order_by('-created_at')

#--------------------------------------------------------------------SALE_ORDER-----------------------


# S.Order contains many products
# S.Order is made by one EMP
class Sale_order(models.Model):
    # customer_name = models.CharField(max_length=255) 
    employee = models.ForeignKey(Employee , related_name="sale_orders", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    products = models.ManyToManyField(Product, related_name="sale_orders")
    # quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Sale_orderManager()
    # products
    # sale_items

# the S.Item table to link the invoice with the product and the quantity of each product in the invoice
class Sale_item(models.Model):
    sale_order = models.ForeignKey(Sale_order, related_name="sale_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="sale_items", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#---------------------Sale--------------------
def create_sale_order(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return Sale_order.objects.create(employee = employee ) # create the invoice

def add_sale_relation(product_id):#------------------------ add the product to the invoice
    product = Product.objects.get(id=product_id)
    sale_order = Sale_order.objects.last()
    return sale_order.products.add(product)
    ################################
def add_item_to_invoice(product_id, quantity):# add the product to the invoice
    product = Product.objects.get(id=product_id)
    sale_order = Sale_order.objects.last()
    return Sale_item.objects.create(sale_order=sale_order, product=product, quantity=quantity)
    #################################
# this is to sale a product
def add_product_to_sale( product_id, quantity ): #--------- minimize the quantity of the product
    product = Product.objects.get(id=product_id)
    product.quantity -= int(quantity)
    return product.save()

def today_sale_orders():#MAI******
    return Sale_order.objects.filter(created_at__contains=datetime.date.today()).count()
def today_purchases():#MAI******
    return Purchasing_invoice.objects.filter(created_at__contains=datetime.date.today()).count()

#--------------------Sale------------------------




#--------------------purchase--------------------
def create_purchase_order(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return Purchasing_invoice.objects.create(employee = employee) # craete the invoice

def add_purchase_relation(product_id): #--------------------------- add the product to the invoice
    product = Product.objects.get(id=product_id)
    purchase_invoice = Purchasing_invoice.objects.last()
    return purchase_invoice.products.add(product)
#################################
def add_item_to_purchase_invoice(product_id, quantity): # add the product to the invoice
    product = Product.objects.get(id=product_id)
    purchase_invoice = Purchasing_invoice.objects.last()
    return Purchase_item.objects.create(purchasing_invoice=purchase_invoice, product=product, quantity=quantity)
#################################
def add_product_to_purchase(product_id, quantity): #--------------- maximize the quantity of the product
    product = Product.objects.get(id=product_id)
    product.quantity += int(quantity)
    return product.save() 
#--------------------purchase--------------------


# this is to purchase a product
def get_all_sales_orders():#--------------------------------------------Mai
    return Sale_order.objects.all().order_by('-created_at')

def get_sale_order(id):#--------------------------------------------Mai
    return Sale_order.objects.get(id=id)
###############################
def sale_orders_products(id):
    sale_order= Sale_order.objects.get(id=id)
    return sale_order.sale_items.all()
###############################


def get_purchase_invoice(id):
    return Purchasing_invoice.objects.get(id=id)

###############################
def purchase_invoices_products(id):
    purchase_invoice= Purchasing_invoice.objects.get(id=id)
    return purchase_invoice.purchase_items.all()
###############################