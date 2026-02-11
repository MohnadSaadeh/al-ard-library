from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import F, ExpressionWrapper, FloatField ,DecimalField, IntegerField
import re
from datetime import datetime , timedelta
import datetime
from .validations import EmployeeManager , ManagerManager , ProductManager , PurchaseManager , Sale_orderManager

# Define pay_choices globally to avoid repetition and NameError
pay_choices = [
    ('cash', _('Cash')),
    ('debts', _('Debts')),
]

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


class CompanyProfile(models.Model):
    """Singleton-ish table to store company profile details used in invoices and headers."""
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=128, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    base_currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, blank=True, related_name='companies_using_as_base')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


def get_company_profile():
    """Return the single CompanyProfile instance if exists, else None."""
    try:
        return CompanyProfile.objects.all().first()
    except Exception:
        return None


def set_company_profile(company_name, registration_number=None, address=None, phone=None, email=None , base_currency=None):
    cp = get_company_profile()
    if cp:
        cp.company_name = company_name or cp.company_name
        cp.registration_number = registration_number or cp.registration_number
        cp.address = address or cp.address
        cp.phone = phone or cp.phone
        cp.email = email or cp.email
        cp.base_currency = base_currency or cp.base_currency
        cp.save()
        return cp
    return CompanyProfile.objects.create(
        company_name=company_name or '',
        registration_number=registration_number or None,
        address=address or None,
        phone=phone or None,
        email=email or None,
        base_currency=base_currency or None,
    )


class Currency(models.Model):
    """Currency model to store supported currencies"""
    code = models.CharField(max_length=3, unique=True)  # ILS, USD, EUR, etc.
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.code} - {self.name}"


class ExchangeRate(models.Model):
    """Exchange rate model to store conversion rates between currencies"""
    from_currency = models.ForeignKey(Currency, related_name='rates_from', on_delete=models.CASCADE)
    to_currency = models.ForeignKey(Currency, related_name='rates_to', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=6)  # e.g., 3.5 for 1 USD = 3.5 ILS
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('from_currency', 'to_currency', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.from_currency.code} to {self.to_currency.code}: {self.rate}"

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
    # manager = models.ForeignKey(Manager , related_name="employees", on_delete=models.CASCADE) 
    is_active = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EmployeeManager()
    # products
    # purchases
    # sale_orders

def add_employee(f_name, l_name, email, DOB, password, confirm_password ):
    # manager = Manager.objects.get(id=manager_id)
    Employee.objects.create(first_name=f_name, last_name=l_name, email=email, DOB=DOB, password=password, confirm_password=confirm_password  )
def get_all_employees():
    return Employee.objects.all()

def get_employee_by_id(id):
    return Employee.objects.get(id=id)






#--------------------------------------------------------------------PRODUCT-----------------------


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    purchasing_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=32, unique=True , null=True, blank=True)
    production_date = models.DateField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)#publisher
    supplier = models.CharField(max_length=255, blank=True, null=True)
    employee = models.ForeignKey(Employee, related_name="products", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()
    # purchases
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
# (المشتريات من الموردين)
# (فاتورة)
class Purchase(models.Model): #i changed from Purchasing_invoice to Purchase >
    employee = models.ForeignKey(Employee , related_name="Purchases", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    # link supplier to this purchase invoice (optional)
    supplier = models.ForeignKey('Supplier', related_name='purchases', on_delete=models.CASCADE, null=True, blank=True)
    # Currency and exchange rate fields
    currency = models.ForeignKey('Currency', related_name='purchases', on_delete=models.SET_NULL, null=True, blank=True)
    exchange_rate_to_base = models.DecimalField(max_digits=10, decimal_places=6, default=1.00)  # rate to convert to base currency
    # إجمالي قيمة الفاتورة
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # the total amount of the invoice
    total_price_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # total in base currency
    payment_method = models.CharField(max_length=10, choices=pay_choices, default='cash')
    
    invoice_pay_method = models.CharField(max_length=10, choices=pay_choices, default='cash')  # Added field
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PurchaseManager()
    # products
    # purchase_items

# the P.Item table to link the invoice with the product and the quantity of each product in the invoice
class Purchase_item(models.Model): # i changed PK name from Purchasing_invoice to Purchase_id >
    purchase_id = models.ForeignKey(Purchase, related_name="purchase_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="purchase_items", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # equal purchasing_price in Product table
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Currency conversion fields
    currency = models.ForeignKey('Currency', related_name='purchase_items', on_delete=models.SET_NULL, null=True, blank=True)
    exchange_rate_to_base = models.DecimalField(max_digits=10, decimal_places=6, default=1.00)
    total_price_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # total in base currency
    # ماذا اشترينا، وبأي كمية، وبأي سعر
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
def get_all_invoices():
    return Purchase.objects.all().order_by('-created_at')

#--------------------------------------------------------------------SALE_ORDER-----------------------


# S.Order contains many products
# S.Order is made by one EMP
# (فاتورة)
class Sale_order(models.Model):
    employee = models.ForeignKey(Employee , related_name="sale_orders", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    # link customer to this sale order (optional)
    customer = models.ForeignKey('Customer', related_name='sales', on_delete=models.CASCADE, null=True, blank=True)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #means the total amount of the order
    exchange_rate_to_base = models.DecimalField(max_digits=10, decimal_places=6, default=1.0)  # Exchange rate to base currency
    total_amount_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total amount in base currency
    invoice_pay_method = models.CharField(max_length=10, choices=pay_choices, default='cash')  # Added field
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Sale_orderManager()
    # products
    # sale_items

# the S.Item table to link the invoice with the product and the quantity of each product in the invoice
# (تفاصيل الفاتورة)
class Sale_item(models.Model):
    sale_order = models.ForeignKey(Sale_order, related_name="sale_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="sale_items", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # equal sale_price in Product table
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # equal sale_price * quantity
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, blank=True, related_name='sale_items')
    exchange_rate_to_base = models.DecimalField(max_digits=10, decimal_places=6, default=1.0)  # Exchange rate to base currency
    total_price_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total price in base currency
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#---------------------Sale--------------------

def create_sale_order(employee_id, customer_id=None):
    employee = Employee.objects.get(id=employee_id)
    customer = None
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            customer = None
    return Sale_order.objects.create(employee=employee, customer=customer)

# def add_sale_relation(product_id):#------------------------ add the product to the invoice
#     product = Product.objects.get(id=product_id)
#     sale_order = Sale_order.objects.last()
#     return sale_order.products.add(product)
    ################################
def add_item_to_invoice(product_id, quantity, sale_price, total_price, currency=None, exchange_rate_to_base=None, total_price_base=None):
    """Create a Sale_item with optional currency/exchange-rate/base-total fields.
    Backwards-compatible with existing callers that only pass 4 args.
    """
    product = Product.objects.get(id=product_id)
    sale_order = Sale_order.objects.last()
    from decimal import Decimal as D

    # Determine currency and exchange rate
    item_currency = currency or sale_order.currency
    ex_rate = D(str(exchange_rate_to_base)) if exchange_rate_to_base is not None else D(str(sale_order.exchange_rate_to_base or 1))

    # Compute base total when not provided
    total_price_decimal = D(str(total_price)) if total_price is not None else D('0')
    total_price_base_val = D(str(total_price_base)) if total_price_base is not None else (total_price_decimal * ex_rate)

    return Sale_item.objects.create(
        sale_order=sale_order,
        product=product,
        quantity=quantity,
        unit_price=sale_price,
        total_price=total_price,
        currency=item_currency,
        exchange_rate_to_base=ex_rate,
        total_price_base=total_price_base_val,
    )
    #################################
# this is to sale a product
def add_product_to_sale( product_id, quantity ): #--------- minimize the quantity of the product
    product = Product.objects.get(id=product_id)
    product.quantity -= int(quantity)
    return product.save()

def today_sale_orders():#MAI******
    return Sale_order.objects.filter(created_at__contains=datetime.date.today()).count()
def today_purchases():#MAI******
    return Purchase.objects.filter(created_at__contains=datetime.date.today()).count()

#--------------------Sale------------------------




#--------------------purchase--------------------
def create_purchase_order(employee_id, supplier_id=None):
    employee = Employee.objects.get(id=employee_id)
    supplier = None
    if supplier_id:
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            supplier = None
    return Purchase.objects.create(employee=employee, supplier=supplier)  # create the invoice

# def add_purchase_relation(product_id): #--------------------------- add the product to the invoice
#     product = Product.objects.get(id=product_id)
#     purchase = Purchase.objects.last()
#     return purchase.products.add(product)
#################################
def add_item_to_purchase_invoice(product_id, quantity ,purchase_price ,total_price ): # add the product to the invoice
    product = Product.objects.get(id=product_id)
    purchase = Purchase.objects.last()
    return Purchase_item.objects.create(purchase_id=purchase, product=product, quantity=quantity , unit_price=purchase_price , total_price=total_price )
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


def get_purchases(id): #changed from get_purchase_invoice to get_purchases
    return Purchase.objects.get(id=id)

###############################
def purchase_invoices_products(id):
    purchase_invoice= Purchase.objects.get(id=id)
    return purchase_invoice.purchase_items.all()
###############################


# ------------------- Returns (Products returned to supplier) -----------------
class Return(models.Model):
    employee = models.ForeignKey(Employee, related_name="returns", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_pay_method = models.CharField(max_length=10, choices=pay_choices, default='cash')  # Added field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Return_item(models.Model):
    return_invoice = models.ForeignKey(Return, related_name="return_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="return_items", on_delete=models.CASCADE)
    # optional link to the original purchase_item row when returning a specific purchase line
    original_item = models.ForeignKey('Purchase_item', null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def create_return_order(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return Return.objects.create(employee=employee)

def add_item_to_return_invoice(product_id, quantity, unit_price, total_price, original_item_id=None):
    product = Product.objects.get(id=product_id)
    return_invoice = Return.objects.last()
    kwargs = {
        'return_invoice': return_invoice,
        'product': product,
        'quantity': quantity,
        'unit_price': unit_price,
        'total_price': total_price,
    }
    if original_item_id:
        try:
            orig = Purchase_item.objects.get(id=original_item_id)
            kwargs['original_item'] = orig
        except Exception:
            pass
    return Return_item.objects.create(**kwargs)


def add_product_to_return(product_id, quantity):
    # subtract returned quantity from product stock
    product = Product.objects.get(id=product_id)
    product.quantity -= int(quantity)
    if product.quantity < 0:
        product.quantity = 0
    return product.save()


def get_all_return_invoices():
    return Return.objects.all().order_by('-created_at')


def get_return_invoice(id):
    return Return.objects.get(id=id)


def return_invoices_products(id):
    return_invoice = Return.objects.get(id=id)
    return return_invoice.return_items.all()


# -------------------- Sale Returns (customer returns) -----------------
class SaleReturn(models.Model):
    # optional link to original sale order if available
    sale_order = models.ForeignKey(Sale_order, related_name='sale_returns', on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, related_name="sale_returns", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_pay_method = models.CharField(max_length=10, choices=pay_choices, default='cash')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SaleReturnItem(models.Model):
    sale_return = models.ForeignKey(SaleReturn, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="sale_return_items", on_delete=models.CASCADE)
    # link to the original sale_item row when returning a specific line
    original_item = models.ForeignKey('Sale_item', null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def create_sale_return(employee_id, sale_order_id=None):
    employee = Employee.objects.get(id=employee_id)
    sale_order = None
    if sale_order_id:
        try:
            sale_order = Sale_order.objects.get(id=sale_order_id)
        except Exception:
            sale_order = None
    # Always set invoice_pay_method to a default value if not provided
    return SaleReturn.objects.create(employee=employee, sale_order=sale_order, invoice_pay_method='cash')


def add_item_to_sale_return(product_id, quantity, unit_price, total_price, original_item_id=None):
    product = Product.objects.get(id=product_id)
    sale_return = SaleReturn.objects.last()
    kwargs = {
        'sale_return': sale_return,
        'product': product,
        'quantity': quantity,
        'unit_price': unit_price,
        'total_price': total_price,
    }
    if original_item_id:
        try:
            orig = Sale_item.objects.get(id=original_item_id)
            kwargs['original_item'] = orig
        except Exception:
            pass
    return SaleReturnItem.objects.create(**kwargs)


def add_product_back_on_return(product_id, quantity):
    product = Product.objects.get(id=product_id)
    product.quantity += int(quantity)
    return product.save()


def get_all_sale_returns():
    return SaleReturn.objects.all().order_by('-created_at')


def get_sale_return(id):
    return SaleReturn.objects.get(id=id)


def sale_return_products(id):
    sr = SaleReturn.objects.get(id=id)
    return sr.items.all()


# Password Reset Token Model
class PasswordResetToken(models.Model):
    user_type = models.CharField(max_length=10, choices=[('employee', 'Employee'), ('manager', 'Manager')])
    user_id = models.IntegerField()
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    



#########################################
class Stock_Out_Voucher(models.Model ):
    employee = models.ForeignKey(Employee , related_name="Stock_Out_Vouchers", on_delete=models.CASCADE) # RESTRICT  deleted >>  dont delete the item or ( default="Default", on_delete=models.SET_DEFAULT)
    # link supplier to this purchase invoice (optional)
    #supplier = models.ForeignKey('Supplier', related_name='Stock_Out_Vouchers', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey('Customer', related_name='Stock_Out_Vouchers', on_delete=models.CASCADE, null=True, blank=True)
    # Currency and exchange rate fields
    currency = models.ForeignKey('Currency', related_name='Stock_Out_Vouchers', on_delete=models.SET_NULL, null=True, blank=True)
    exchange_rate_to_base = models.DecimalField(max_digits=10, decimal_places=6, default=1.00)  # rate to convert to base currency
    # إجمالي قيمة الفاتورة
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # the total amount of the invoice
    total_price_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # total in base currency
    payment_method = models.CharField(max_length=10, choices=pay_choices, default='cash')
    
    invoice_pay_method = models.CharField(max_length=10, choices=pay_choices, default='cash')  # Added field
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = Stock_Out_VouchersManager()
    
    # products
    # purchase_items
    
    
#########################################

#########################################
class Stock_Out_Voucher_item(models.Model):
    Stock_Out_Voucher_id = models.ForeignKey(Stock_Out_Voucher, related_name="Stock_Out_Voucher_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="Stock_Out_Voucher_items", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # equal purchasing_price in Product table
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Currency conversion fields
    currency = models.ForeignKey('Currency', related_name='Stock_Out_Voucher_items', on_delete=models.SET_NULL, null=True, blank=True)
    exchange_rate_to_base = models.DecimalField(max_digits=10, decimal_places=6, default=1.00)
    total_price_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # total in base currency
    # ماذا اشترينا، وبأي كمية، وبأي سعر
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

#########################################

def get_all_Stock_Out_Vouchers():
    return Stock_Out_Voucher.objects.all().order_by('-created_at')
def get_allStock_Out_Voucher_item():
    return Stock_Out_Voucher_item.objects.all().order_by('-created_at')
