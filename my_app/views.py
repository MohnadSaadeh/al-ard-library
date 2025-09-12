from django.shortcuts import render ,redirect
from . import models
from django.contrib import messages
import bcrypt
from datetime import datetime , timedelta
import datetime
from django.db.models import Sum
from django.db.models.functions import ExtractWeekDay
from django.http import JsonResponse
from . import validations


# to display the sign-in page
def about_us(request):
    return render(request, 'about_us.html')




def display_homepage(request):
    return render(request, 'sign-in.html')

def index(request):
    if 'employee_id' in request.session:
        context = {   
            'segment': index,        
            'sixmonthesproducts': models.get_six_monthes_products(), # MAI ******
            'near_expiry':models.get_six_monthes(),   # MAI ******        
            'out_stock':models.out_of_stock(),
            'count':models.count_out_stock(),
            'today_sale_order':models.today_sale_orders(), #MAI *******
            'today_purchases_order' : models.today_purchases(),
            'employee': models.get_employee_by_id(request.session['employee_id']),

            # 'chart_data':models.chart_sales_orders()
            # 'saturday' : models.Sale_order.objects.filter(created_at__contains__week_day=7).count(),
            'monday' : models.Sale_order.objects.filter(created_at__week_day=2).count(),
            'tuseday' : models.Sale_order.objects.filter(created_at__week_day=3).count(),
            'wednesday' : models.Sale_order.objects.filter(created_at__week_day=4).count(),
            'thurseday' : models.Sale_order.objects.filter(created_at__week_day=5).count(),
            'friday' : models.Sale_order.objects.filter(created_at__week_day=6).count(),
            'saturday' : models.Sale_order.objects.filter(created_at__week_day=7).count(),
            'sunday' : models.Sale_order.objects.filter(created_at__week_day=1).count(),

            # 'employees' : active_employees,
            

            }
        return render(request , 'index.html' , context)
    else:
        return redirect('/')
    

def sign_up(request):
    return render(request , 'sign-up.html' )

# if anyone want to Sign is
def sign_in(request):
    if request.method == 'POST':
        # if he is an EMPLOYEE
        if request.POST['account_type'] == "1" : # Emoployee
            errors = models.Employee.objects.login_employee_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value )
                return redirect('/')
            else:
                employee_email = request.POST['email'] # here we get the email thet ENSERTED
                employee_password = request.POST['password'] # here we get the password thet ENSERTED
                employee = models.Employee.objects.filter(email=employee_email) # here we get the EMPLOYEE by the email from DB
                if employee: # here we check if the EMPLOYEE exist
                    employee_user = employee[0] # here we get the EMPLOYEE from the list
                    if bcrypt.checkpw(employee_password.encode(), employee_user.password.encode()): # here we chick the password 
                        request.session['employee_id'] = employee_user.id
                        #---------------is Active -----------------------
                        employee = models.Employee.objects.get(id=request.session['employee_id'])
                        employee.is_active = True
                        employee.save()
                        #---------------is Active -----------------------
                        return redirect('/index')
                    else:
                        messages.error(request, "Incorrect Password")
                        # messages.error(request, value , extra_tags = 'admin_login' )
                        return redirect('/')
                messages.error(request, "Email is incorrect")
                return redirect('/')
        # if he is a MANAGER
        else:
            if request.POST['account_type'] == "2" : # Manager
                errors = models.Manager.objects.login_manager_validator(request.POST)
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value )
                    return redirect('/')
                else:
                    manager_email = request.POST['email'] # here we get the email thet ENSERTED
                    manager_password = request.POST['password'] # here we get the password thet ENSERTED
                    manager = models.Manager.objects.filter(email=manager_email) # here we get the MANAGER by the email from DB
                    if manager: # here we check if the MANAGER exist
                        manager_user = manager[0] # here we get the MANAGER from the list
                        #ADDING MANAGER FROME ADMIN
                        if manager_password == manager_user.password :
                            request.session['manager_id'] = manager_user.id
                            return redirect('/index')
                        else:
                            messages.error(request, "Incorrect Password")
                            # messages.error(request, value , extra_tags = 'admin_login' )
                            return redirect('/')
                    messages.error(request, "Email is incorrect")
    else:
        return redirect('/')

                #     if bcrypt.checkpw(manager_password.encode(), manager_user.password.encode()): # here we chick the password 
                #         request.session['manager_id'] = manager_user.id
                #         return redirect('/index')
                #     else:
                #         messages.error(request, "Incorrect Password")
                #         # messages.error(request, value , extra_tags = 'admin_login' )
                #         return redirect('/')
                # messages.error(request, "Email is incorrect")
                # return redirect('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
def emp_logout(request):
    employee = models.Employee.objects.get(id=request.session['employee_id'])
    employee.is_active = False
    employee.save()
    request.session.clear()
    return redirect('/')

def display_stock_for_manager(request):
    context={
        'products': models.get_all_products(),
        'today': datetime.date.today(),
        'expiry_range': datetime.date.today() + timedelta(days=6*30),
    }
    return render(request, 'stock_manager.html',context)


def add_new_employee(request):
    errors = models.Employee.objects.employee_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/employees')
    else:
        # manager = request.session['manager_id']
        manager = request.session['employee_id'] # or manager_id
        emp_f_name = request.POST['f_name']
        emp_l_name = request.POST['l_name']
        emp_emeil = request.POST['email']
        emp_DOB = request.POST['DOB']
        emp_password = request.POST['password']
        emp_conf_password = request.POST['c_password']
        #hash-----Passwords-------
        pw_hash = bcrypt.hashpw(emp_password.encode(), bcrypt.gensalt()).decode()
        pw_hash_confirm = bcrypt.hashpw(emp_conf_password.encode(), bcrypt.gensalt()).decode()
        #hash-----Passwords-------
        models.add_employee(emp_f_name, emp_l_name, emp_emeil, emp_DOB, pw_hash, pw_hash_confirm , manager )
        messages.success(request, "Successfully added an employee!" , extra_tags = 'add_employee')
        return redirect('/employees')

def display_employees(request):
    # if the manad=egr not in the loged on
    # 'manager_id' or 'employee_id' in request.session:
    if 'employee_id' not in request.session:
        return redirect('/index')
    else:
        context = {
            'employees': models.get_all_employees(),
            'employee': models.get_employee_by_id(request.session['employee_id']),

        }
        return render (request, 'profile.html', context )



def display_employee_dashboard(request):
    if 'employee_id' not in request.session:
        return redirect('/index')
    else:
        context = {
            'products': models.get_all_products(),
            'employee': models.get_employee_by_id(request.session['employee_id'])
        }
        return render(request, 'tables.html' , context )



def add_new_product(request):
    errors = models.Product.objects.product_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/employye_dashboard')
    else:
        employee = request.session['employee_id']
        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        purchasing_price = request.POST['purchasing_price']
        expiry_date = request.POST['expiry_date']
        supplier = request.POST['supplier']
        models.add_product(product_name, quantity, purchasing_price, expiry_date, supplier, employee)
        messages.success(request, "Successfully added a product!", extra_tags = 'add_product')
        return redirect('/employye_dashboard')



def display_sales(request):
    context = {
            'sale_order': sale_order,
            'products': models.get_all_products(),
            'orders' : models.get_all_sales_orders(),
            'employee': models.get_employee_by_id(request.session['employee_id'])
        }
    return render(request , 'sale_orders.html', context )

def display_purchases(request):
    context = {
            'purchases_order': purchases_order,
            'products': models.get_all_products(),#--------------------------------------------Mai
            'invoices' : models.get_all_invoices(),
            'employee': models.get_employee_by_id(request.session['employee_id']),#--------------------------------------------Mai
        }
    return render(request , 'purchase_invoices.html' ,context)

def delete_product(request):
    models.delete_clicked_product(request)
    return redirect('/employye_dashboard')


sale_order = []
#____________________________________SALE___________________________________
def add_product_to_sale(request):
    errors = models.Sale_order.objects.invoice_sale_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/sales')
    else:
        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        product_id = models.Product.objects.get(product_name=product_name).id
        sale_order.append ( {'product_name': product_name , 'product_id': product_id , 'quantity': quantity } )
        return redirect('/sales')
    
def submet_sale_order(request):
    if sale_order == []:
        messages.error(request, "Please add at least one product to sale!")
        return redirect('/sales')
    else:
        employee_id = request.session['employee_id']
        models.create_sale_order(employee_id) #---------CREATE the invoise------- 1

        for key in sale_order :
            product_name = key.get('product_name')
            product_id = key.get('product_id')
            quantity = key.get('quantity')
            #make invoice                                        
            models.add_sale_relation(product_id)#---------GET the product-----AMD------ADD the product------- 4
            ###############################
            models.add_item_to_invoice(product_id, quantity)#new
            ##############################
            models.add_product_to_sale( product_id, quantity )
            
        sale_order.clear()
        messages.success(request, "Successfully Sold!", extra_tags = 'sold_product')

        return redirect('/sales')
#____________________________________SALE___________________________________

purchases_order = []
#____________________________________PURCHASE___________________________________
def add_product_to_purchase(request):
    errors = models.Purchasing_invoice.objects.invoice_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/purchases')
    else:
        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        product_id = models.Product.objects.get(product_name=product_name).id
        purchases_order.append ( {'product_name': product_name, 'product_id': product_id , 'quantity': quantity} )
        return redirect('/purchases')
    
def submet_purchase_order(request):
    if purchases_order == []:
        messages.error(request, "Please add at least one product to purchase!")
        return redirect('/purchases')
    else:
        employee_id = request.session['employee_id']
        models.create_purchase_order(employee_id) #---------CREATE the invoise------- 1
        for key in purchases_order :
            product_name = key.get('product_name')
            product_id = key.get('product_id')
            quantity = key.get('quantity')
            
            models.add_purchase_relation(product_id)#---------GET the product-----AMD------ADD the product------- 4
            #################################
            models.add_item_to_purchase_invoice(product_id, quantity)
            #################################
            models.add_product_to_purchase(product_id, quantity)
        purchases_order.clear()
        messages.success(request, "Purchased Successfully!", extra_tags = 'add_invoice')

        return redirect('/purchases')
#____________________________________PURCHASE___________________________________

def clear_purchases_list(request):
    if purchases_order == []:
        messages.error(request, "already empty!")
        return redirect('/purchases')
    else:
        purchases_order.clear()
        return redirect('/purchases')

    return purchases_order.clear()

def clear_sales_list(request) :
    if sale_order == []:
        messages.error(request, "already empty!")
        return redirect('/sales')
    else:
        sale_order.clear()
        return redirect('/sales')

def display_employee_reports(request):
    context = {
        'products': models.get_all_products(),
        'today': datetime.date.today(),
        'expiry_range': datetime.date.today() + timedelta(days=6*30),
        'employee': models.get_employee_by_id(request.session['employee_id'])
    }
    return render (request, 'employee_reports.html', context)

def view_sale_order(request, id):#--------------------------------------------Mai
    context={
        'order': models.get_sale_order(id),
        ###############################
        'sale_products':models.sale_orders_products(id),#MAI*****
        ###############################
        
    }
    return render(request, 'view_sale_order.html',context)

def view_purchase_invoice(request,id):
    context={
        'order': models.get_sale_order(id),
        'invoice': models.get_purchase_invoice(id),
        'purchase_products':models.purchase_invoices_products(id),#MAI*****
    }
    return render(request, 'view_purchase_invoice.html',context)

def display_edit_form(request,id):
    context={
        'products': models.get_all_products(),
        'product':models.get_product(id),
        'employee': models.get_employee_by_id(request.session['employee_id'])
    }
    return render(request, 'edit_product.html',context)

def update_product(request,id):
    errors = models.Product.objects.product_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_product/{id}')
    else:
        models.update_selected_product(request,id)

    return redirect('/employye_dashboard')#--------------------------------------------Mai


def get_date_time():
    return datetime.date.today()# used in models line 69

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt   # only if you want to test without CSRF
def search_results(request):
    if 'employee_id' not in request.session:
        return redirect('/index')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        searchValue = request.POST.get('searchValue', '')
        qs = models.Product.objects.filter(product_name__icontains=searchValue)

        if qs.exists() and len(searchValue) > 0:
            data = []
            for pos in qs:
                data.append({
                    'id': pos.id,
                    'product_name': pos.product_name,
                    'quantity': pos.quantity,
                    'purchasing_price': str(pos.purchasing_price),  # safe for JSON
                    'expiry_date': pos.expiry_date.strftime('%Y-%m-%d') if pos.expiry_date else '',
                    'supplier': str(pos.supplier),
                })
            return JsonResponse({'data': data})
        else:
            return JsonResponse({'data': 'No Products found ...'})

    return JsonResponse({})







def get_active_users(request):
    active_users = models.Employee.objects.filter(is_active=True).values('first_name' , 'last_name')
    return JsonResponse({'active_users': list(active_users)})




from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductAttribute
from .forms import ProductForm, ProductAttributeFormSet

def product_create(request):
    """
    إنشاء منتج جديد مع خصائصه (Attributes) باستخدام formset
    """
    # جلب معرف الموظف من السيشن (إذا موجود)
    employee_id = request.session.get('employee_id')

    if request.method == "POST":
        form = ProductForm(request.POST)
        formset = ProductAttributeFormSet(request.POST, queryset=ProductAttribute.objects.none())
        
        if form.is_valid() and formset.is_valid():
            # حفظ المنتج وربطه بالموظف
            product = form.save(commit=False)
            if employee_id:
                product.employee_id = employee_id
            product.save()

            # حفظ الخصائص وربطها بالمنتج
            formset.instance = product
            formset.save()

            return redirect('product_list')  # تأكد أن لديك URL اسمه product_list
    else:
        form = ProductForm()
        formset = ProductAttributeFormSet(queryset=ProductAttribute.objects.none())

    return render(request, 'products/product_form.html', {
        'form': form,
        'formset': formset
    })


def product_list(request):
    """
    عرض قائمة المنتجات مع خصائصها
    """
    products = Product.objects.all().prefetch_related('attributes')
    return render(request, 'products/product_list.html', {'products': products})




def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        formset = ProductAttributeFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        formset = ProductAttributeFormSet(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'formset': formset})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
