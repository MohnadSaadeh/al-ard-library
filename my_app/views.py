from django.shortcuts import render ,redirect
from . import models
from django.contrib import messages
import bcrypt
from datetime import datetime , timedelta
import datetime
from django.db.models import Sum
from django.db import transaction
from django.db.models.functions import ExtractWeekDay
from django.http import JsonResponse
from . import validations
from django.core.paginator import Paginator
from django.utils.translation import gettext as _



# Session-backed cart helpers (per-user carts stored in session)
def _get_sale_cart(request):
    return request.session.get('sale_order', [])


def _save_sale_cart(request, cart):
    request.session['sale_order'] = cart
    request.session.modified = True


def _get_purchase_cart(request):
    return request.session.get('purchases_order', [])


def _save_purchase_cart(request, cart):
    request.session['purchases_order'] = cart
    request.session.modified = True


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
        return redirect('/signup')
    else:
        # manager = request.session['manager_id']
        # manager = request.session['employee_id'] # or manager_id
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
        models.add_employee(emp_f_name, emp_l_name, emp_emeil, emp_DOB, pw_hash, pw_hash_confirm  )
        messages.success(request, "Successfully added an employee!" , extra_tags = 'add_employee')
        return redirect('/signup')

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
    # calculate grand total for current sale order (session-backed)
    cart = _get_sale_cart(request)
    grand_total = sum(float(item.get('total_price', 0)) for item in cart)
    # paginate recent sales orders
    orders_qs = models.get_all_sales_orders()
    orders_page_number = request.GET.get('orders_page')
    orders_paginator = Paginator(orders_qs, 10)  # 10 orders per page
    orders_page = orders_paginator.get_page(orders_page_number)

    context = {
            'sale_order': cart,
            'products': models.get_all_products(),
            'orders' : orders_page,
            'employee': models.get_employee_by_id(request.session['employee_id']),
            'grand_total': grand_total,
            'orders_paginator': orders_paginator,
        }
    return render(request , 'sale_orders.html', context )

def display_purchases(request):
    # calculate grand total (session-backed)
    p_cart = _get_purchase_cart(request)
    grand_total = sum(float(item.get('total_price', 0)) for item in p_cart)
    # paginate recent purchase invoices
    invoices_qs = models.get_all_invoices()
    invoices_page_number = request.GET.get('invoices_page')
    invoices_paginator = Paginator(invoices_qs, 10)  # 10 invoices per page
    invoices_page = invoices_paginator.get_page(invoices_page_number)

    context = {
            'purchases_order': p_cart,
            'products': models.get_all_products(),#--------------------------------------------Mai
            'invoices' : invoices_page,
            'employee': models.get_employee_by_id(request.session['employee_id']),#--------------------------------------------Mai
            'grand_total': grand_total,
            'invoices_paginator': invoices_paginator,
        }
    return render(request , 'purchase_invoices.html' ,context)

def delete_product(request):
    models.delete_clicked_product(request)
    return redirect('/employye_dashboard')


# session-backed sale_order is stored per-user in request.session via helpers above
#____________________________________SALE___________________________________
def add_product_to_sale(request):
    errors = models.Sale_order.objects.invoice_sale_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/sales')
    else:
        product_name = request.POST['product_name']
        quantity = int(request.POST['quantity'])
        product = models.Product.objects.get(product_name=product_name)
        product_id = product.id
        sale_price = float(product.sale_price) if product.sale_price is not None else 0.0
        total_price = quantity * sale_price
        cart = _get_sale_cart(request)
        cart.append({'product_name': product_name, 'product_id': product_id, 'quantity': quantity, 'sale_price': sale_price, 'total_price': total_price})
        _save_sale_cart(request, cart)
        return redirect('/sales')
    

def scan_add_to_sale(request):
    """
    AJAX endpoint: receive 'isbn' (POST) from scanner and add product to sale_order list.
    Returns JSON with status and rendered HTML snippet for the order summary.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    isbn = request.POST.get('isbn', '').strip()
    if not isbn:
        return JsonResponse({'status': 'error', 'message': 'No ISBN provided'}, status=400)

    try:
        product = models.Product.objects.get(isbn=isbn)
    except Exception:
        return JsonResponse({'status': 'not_found', 'message': 'Product not found'})

    # find existing session-backed sale_order list and increment or add
    cart = _get_sale_cart(request)
    for item in cart:
        if int(item.get('product_id')) == int(product.id):
            item['quantity'] = int(item.get('quantity', 0)) + 1
            try:
                item['total_price'] = int(item['quantity']) * float(item.get('sale_price', 0))
            except Exception:
                item['total_price'] = 0
            break
    else:
        sale_price = float(product.sale_price) if product.sale_price is not None else 0.0
        cart.append({
            'product_name': product.product_name,
            'product_id': product.id,
            'quantity': 1,
            'sale_price': sale_price,
            'total_price': sale_price,
        })

    _save_sale_cart(request, cart)

    # compute grand total
    grand_total = sum(float(item.get('total_price', 0)) for item in cart)

    # return simplified JSON payload; front-end will re-render
    return JsonResponse({'status': 'ok', 'grand_total': grand_total, 'items': cart})

def submet_sale_order(request):
    cart = _get_sale_cart(request)
    if not cart:
        messages.error(request, "Please add at least one product to sale!")
        return redirect('/sales')
    else:
        employee_id = request.session['employee_id']
        models.create_sale_order(employee_id) #---------CREATE the invoise------- 1

        for key in cart:
            product_id = key.get('product_id')
            quantity = int(key.get('quantity'))
            models.add_item_to_invoice(product_id, quantity)
            models.add_product_to_sale(product_id, quantity)

        # update the created Sale_order total_amount by summing sale items
        try:
            last_sale = models.Sale_order.objects.last()
            total_sum = models.Sale_item.objects.filter(sale_order=last_sale).aggregate(total=Sum('total_price'))['total'] or 0
            last_sale.total_amount = total_sum
            last_sale.save()
        except Exception:
            pass

        _save_sale_cart(request, [])
        messages.success(request, "Successfully Sold!", extra_tags = 'sold_product')

        return redirect('/sales')
#____________________________________SALE___________________________________


# -------------------- Sales Return (customer returns) --------------------
def sale_return_create_view(request, sale_order_id):
    # ensure employee logged in
    if 'employee_id' not in request.session:
        messages.error(request, 'Please sign in to create a return.')
        return redirect('/')

    try:
        sale_order = models.Sale_order.objects.get(id=sale_order_id)
    except models.Sale_order.DoesNotExist:
        messages.error(request, 'Sale order not found.')
        return redirect('/sales')

    # build items with allowed return quantities (per original sale_item)
    items = []
    for si in sale_order.sale_items.all():
        returned_qty = models.SaleReturnItem.objects.filter(original_item=si).aggregate(total=Sum('quantity'))['total'] or 0
        allowed = max(0, si.quantity - int(returned_qty))
        items.append({
            'sale_item': si,
            'product': si.product,
            'sold_quantity': si.quantity,
            'unit_price': si.unit_price,
            'allowed_return_quantity': allowed,
        })

    if request.method == 'POST':
        # collect requested returns
        requested = []
        for entry in items:
            si = entry['sale_item']
            key = f'return_qty_{si.id}'
            qty_str = request.POST.get(key, '0')
            try:
                qty = int(qty_str)
            except ValueError:
                qty = 0
            if qty > 0:
                if qty > entry['allowed_return_quantity']:
                    messages.error(request, f'Cannot return {qty} of {si.product.product_name}; only {entry["allowed_return_quantity"]} available to return.')
                    return redirect(request.path)
                requested.append((si, qty))

        if not requested:
            messages.error(request, 'Please enter at least one quantity to return.')
            return redirect(request.path)

        # create SaleReturn and items
        employee_id = request.session['employee_id']
        # use Django transaction when available
        with transaction.atomic():
            # use helper to create return (keeps consistency with existing code)
            models.create_sale_return(employee_id, sale_order_id)
            for si, qty in requested:
                unit_price = float(si.unit_price or 0)
                total_price = qty * unit_price
                models.add_item_to_sale_return(si.product.id, qty, unit_price, total_price, original_item_id=si.id)
                # increase stock on return
                models.add_product_back_on_return(si.product.id, qty)

            # update totals on the created SaleReturn
            try:
                grand = sum(qty * float(si.unit_price or 0) for si, qty in requested)
            except Exception:
                grand = 0.0
            last_sr = models.SaleReturn.objects.last()
            if last_sr:
                last_sr.grand_total = grand
                last_sr.total_amount = grand
                last_sr.save()

        messages.success(request, 'Sale return recorded.', extra_tags='sale_return')
        return redirect(f'/sales/returns/{ last_sr.id }')

    context = {
        'sale_order': sale_order,
        'items': items,
        'employee': models.get_employee_by_id(request.session['employee_id']) if 'employee_id' in request.session else None,
    }
    return render(request, 'sales/sale_return_form.html', context)


def sale_return_detail_view(request, id):
    try:
        sr = models.SaleReturn.objects.get(id=id)
    except models.SaleReturn.DoesNotExist:
        messages.error(request, 'Sale return not found.')
        return redirect('/sales')

    items = sr.items.select_related('product', 'original_item').all()
    total = items.aggregate(total=Sum('total_price'))['total'] or 0
    context = {
        'sale_return': sr,
        'items': items,
        'total': total,
    }
    return render(request, 'sales/sale_return_detail.html', context)


# -------------------- Purchase Return (supplier returns) --------------------
def purchase_return_create_view(request, purchase_id):
    if 'employee_id' not in request.session:
        messages.error(request, 'Please sign in to create a return.')
        return redirect('/')

    try:
        purchase = models.Purchase.objects.get(id=purchase_id)
    except models.Purchase.DoesNotExist:
        messages.error(request, 'Purchase not found.')
        return redirect('/purchases')

    items = []
    for pi in purchase.purchase_items.all():
        returned_qty = models.Return_item.objects.filter(original_item=pi).aggregate(total=Sum('quantity'))['total'] or 0
        allowed = max(0, pi.quantity - int(returned_qty))
        items.append({
            'purchase_item': pi,
            'product': pi.product,
            'purchased_quantity': pi.quantity,
            'unit_price': pi.unit_price,
            'allowed_return_quantity': allowed,
        })

    if request.method == 'POST':
        requested = []
        for entry in items:
            pi = entry['purchase_item']
            key = f'return_qty_{pi.id}'
            qty_str = request.POST.get(key, '0')
            try:
                qty = int(qty_str)
            except ValueError:
                qty = 0
            if qty > 0:
                if qty > entry['allowed_return_quantity']:
                    messages.error(request, f'Cannot return {qty} of {pi.product.product_name}; only {entry["allowed_return_quantity"]} available to return.')
                    return redirect(request.path)
                requested.append((pi, qty))

        if not requested:
            messages.error(request, 'Please enter at least one quantity to return.')
            return redirect(request.path)

        employee_id = request.session['employee_id']
        with transaction.atomic():
            models.create_return_order(employee_id)
            for pi, qty in requested:
                unit_price = float(pi.unit_price or 0)
                total_price = qty * unit_price
                models.add_item_to_return_invoice(pi.product.id, qty, unit_price, total_price, original_item_id=pi.id)
                # For purchase returns, decrease stock because products are returned to supplier
                models.add_product_to_return(pi.product.id, qty)

            try:
                grand = sum(qty * float(pi.unit_price or 0) for pi, qty in requested)
            except Exception:
                grand = 0.0
            last_r = models.Return.objects.last()
            if last_r:
                last_r.grand_total = grand
                last_r.total_amount = grand
                last_r.save()

        messages.success(request, 'Purchase return recorded.', extra_tags='return_purchase')
        return redirect(f'/purchases/returns/{ last_r.id }')

    context = {
        'purchase': purchase,
        'items': items,
        'employee': models.get_employee_by_id(request.session['employee_id']) if 'employee_id' in request.session else None,
    }
    return render(request, 'purchases/purchase_return_form.html', context)


def purchase_return_detail_view(request, id):
    try:
        r = models.Return.objects.get(id=id)
    except models.Return.DoesNotExist:
        messages.error(request, 'Return not found.')
        return redirect('/purchases')

    items = r.return_items.select_related('product', 'original_item').all()
    total = items.aggregate(total=Sum('total_price'))['total'] or 0
    context = {
        'return': r,
        'items': items,
        'total': total,
    }
    return render(request, 'purchases/purchase_return_detail.html', context)



# session-backed purchases_order is stored per-user in request.session via helpers above
#____________________________________PURCHASE___________________________________
def add_product_to_purchase(request):
    errors = models.Purchase.objects.invoice_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/purchases')
    else:
        product_name = request.POST['product_name']
        quantity = int(request.POST['quantity'])
        prod = models.Product.objects.get(product_name=product_name)
        product_id = prod.id
        purchase_price = float(prod.purchasing_price) if prod.purchasing_price is not None else 0.0
        total_price = quantity * purchase_price
        cart = _get_purchase_cart(request)
        cart.append({
            'product_name': product_name,
            'product_id': product_id,
            'quantity': quantity,
            'purchase_price': purchase_price,
            'total_price': total_price,
        })
        _save_purchase_cart(request, cart)
        return redirect('/purchases')
    

def scan_add_to_purchase(request):
    """
    AJAX endpoint: receive 'isbn' (POST) from scanner and add product to purchases_order list.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    isbn = request.POST.get('isbn', '').strip()
    if not isbn:
        return JsonResponse({'status': 'error', 'message': 'No ISBN provided'}, status=400)

    try:
        product = models.Product.objects.get(isbn=isbn)
    except Exception:
        return JsonResponse({'status': 'not_found', 'message': 'Product not found'})

    cart = _get_purchase_cart(request)
    for item in cart:
        if int(item.get('product_id')) == int(product.id):
            item['quantity'] = int(item.get('quantity', 0)) + 1
            try:
                item['total_price'] = int(item['quantity']) * float(item.get('purchase_price', 0))
            except Exception:
                item['total_price'] = 0
            break
    else:
        purchase_price = float(product.purchasing_price) if product.purchasing_price is not None else 0.0
        # read session-backed purchases cart
        cart = _get_purchase_cart(request)
        # if item wasn't found in loop above, append
        cart.append({
            'product_name': product.product_name,
            'product_id': product.id,
            'quantity': 1,
            'purchase_price': purchase_price,
            'total_price': purchase_price,
        })

        _save_purchase_cart(request, cart)

    # compute grand total from session cart
    cart = _get_purchase_cart(request)
    grand_total = sum(float(item.get('total_price', 0)) for item in cart)
    return JsonResponse({'status': 'ok', 'grand_total': grand_total, 'items': cart})
    
def submet_purchase_order(request):
    cart = _get_purchase_cart(request)
    if not cart:
        messages.error(request, "Please add at least one product to purchase!")
        return redirect('/purchases')
    else:
        employee_id = request.session['employee_id']
        models.create_purchase_order(employee_id) #---------CREATE the invoise------- 1
        for key in cart:
            product_id = key.get('product_id')
            quantity = int(key.get('quantity'))
            purchase_price = float(key.get('purchase_price') or 0)
            total_price = float(key.get('total_price') or 0)
            models.add_item_to_purchase_invoice(product_id, quantity, purchase_price, total_price)
            models.add_product_to_purchase(product_id, quantity)

        # update the created Purchase total (grand_total and total_amount)
        try:
            last_purchase = models.Purchase.objects.last()
            total_sum = models.Purchase_item.objects.filter(purchase_id=last_purchase).aggregate(total=Sum('total_price'))['total'] or 0
            last_purchase.grand_total = total_sum
            last_purchase.total_amount = total_sum
            last_purchase.save()
        except Exception:
            pass

        _save_purchase_cart(request, [])
        messages.success(request, "Purchased Successfully!", extra_tags = 'add_invoice')

        return redirect('/purchases')
#____________________________________PURCHASE___________________________________

def clear_purchases_list(request):
    cart = _get_purchase_cart(request)
    if not cart:
        messages.error(request, "already empty!")
        return redirect('/purchases')
    _save_purchase_cart(request, [])
    return redirect('/purchases')


# -------------------- RETURN PURCHASES (Products returned) --------------------
returns_order = []

def display_returns(request):
    # calculate grand total for current return order
    grand_total = sum(item['total_price'] for item in returns_order)
    context = {
        'returns_order': returns_order,
        'products': models.get_all_products(),
        'return_invoices': models.get_all_return_invoices(),
        'employee': models.get_employee_by_id(request.session['employee_id']),
        'grand_total': grand_total,
    }
    return render(request, 'return_purchases.html', context)


def add_product_to_return(request):
    errors = models.Purchase.objects.invoice_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/return_purchases')
    else:
        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        product = models.Product.objects.get(product_name=product_name)
        product_id = product.id
        unit_price = product.purchasing_price
        total_price = int(quantity) * float(unit_price)
        returns_order.append({
            'product_name': product_name,
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price,
        })
        # immediately subtract quantity from product stock in memory via model helper
        models.add_product_to_return(product_id, quantity)
        return redirect('/return_purchases')


def submet_return_order(request):
    if returns_order == []:
        messages.error(request, "Please add at least one product to return!")
        return redirect('/return_purchases')
    else:
        employee_id = request.session['employee_id']
        models.create_return_order(employee_id)
        for key in returns_order:
            product_id = key.get('product_id')
            quantity = key.get('quantity')
            unit_price = key.get('unit_price')
            total_price = key.get('total_price')
            models.add_item_to_return_invoice(product_id, quantity, unit_price, total_price)
            # Already subtracted when adding to cart, so no need to call again

        # compute grand_total from the items we've just added
        try:
            grand = sum(float(item.get('total_price')) for item in returns_order)
        except Exception:
            grand = 0.0
        # update grand_total on the created return invoice
        last_return = models.Return.objects.last()
        if last_return:
            last_return.grand_total = grand
            last_return.total_amount = grand
            last_return.save()

        returns_order.clear()
        messages.success(request, "Return Recorded Successfully!", extra_tags='add_return')
        return redirect('/return_purchases')


def clear_returns_list(request):
    if returns_order == []:
        messages.error(request, "already empty!")
        return redirect('/return_purchases')
    else:
        # If user clears the list, we should restore quantities back to stock
        for item in returns_order:
            try:
                models.add_product_to_purchase(item.get('product_id'), item.get('quantity'))
            except Exception:
                pass
        returns_order.clear()
        return redirect('/return_purchases')


def view_return_invoice(request, id):
    context = {
        'invoice': models.get_return_invoice(id),
        'return_products': models.return_invoices_products(id),
    }
    return render(request, 'view_return_invoice.html', context)


# ---------- Sale Returns (customer returns) session-backed cart

def _get_sale_returns_cart(request):
    return request.session.get('sale_returns_cart', [])


def _save_sale_returns_cart(request, cart):
    request.session['sale_returns_cart'] = cart
    request.session.modified = True


def display_sale_returns(request):
    cart = _get_sale_returns_cart(request)
    # ensure numeric floats for display
    grand_total = sum(float(item.get('total_price', 0)) for item in cart)
    context = {
        'sale_returns_cart': cart,
        'products': models.get_all_products(),
        'sale_returns': models.get_all_sale_returns(),
        'employee': models.get_employee_by_id(request.session['employee_id']),
        'grand_total': grand_total,
    }
    return render(request, 'return_sales.html', context)


def add_product_to_sale_return(request):
    errors = models.Purchase.objects.invoice_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/return_sales')
    else:
        product_name = request.POST['product_name']
        quantity = int(request.POST['quantity'])
        product = models.Product.objects.get(product_name=product_name)
        product_id = product.id
        unit_price = float(product.sale_price) if product.sale_price is not None else 0.0
        total_price = quantity * float(unit_price)

        cart = _get_sale_returns_cart(request)
        cart.append({
            'product_name': product_name,
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': float(unit_price),
            'total_price': float(total_price),
        })
        _save_sale_returns_cart(request, cart)

        # restock the product immediately
        models.add_product_back_on_return(product_id, quantity)
        return redirect('/return_sales')


def submit_sale_return(request):
    cart = _get_sale_returns_cart(request)
    if not cart:
        messages.error(request, "Please add at least one product to return!")
        return redirect('/return_sales')
    else:
        from django.db import transaction
        employee_id = request.session['employee_id']
        sale_order_id = request.POST.get('sale_order_id') if request.method == 'POST' else None

        # If a sale_order_id was chosen, validate each cart item belongs to that sale and quantity <= allowed (sold - already returned)
        if sale_order_id:
            try:
                so = models.Sale_order.objects.get(id=sale_order_id)
            except Exception:
                messages.error(request, "Selected sale order not found.")
                return redirect('/return_sales')

            # build sold map and already-returned map
            sold_qs = models.Sale_item.objects.filter(sale_order=so).values('product_id').annotate(total=Sum('quantity'))
            sold_map = {row['product_id']: int(row['total'] or 0) for row in sold_qs}
            returned_qs = models.SaleReturnItem.objects.filter(sale_return__sale_order=so).values('product_id').annotate(total=Sum('quantity'))
            returned_map = {row['product_id']: int(row['total'] or 0) for row in returned_qs}

            for item in cart:
                pid = item.get('product_id')
                requested = int(item.get('quantity'))
                sold = sold_map.get(pid, 0)
                already = returned_map.get(pid, 0)
                allowed = max(0, sold - already)
                if sold == 0:
                    messages.error(request, f"Product id {pid} is not part of sale invoice #{sale_order_id}.")
                    return redirect('/return_sales')
                if requested > allowed:
                    messages.error(request, f"Cannot return {requested} of product id {pid}; only {allowed} remaining from invoice #{sale_order_id}.")
                    return redirect('/return_sales')

        # Passed validations; create SaleReturn and items inside a transaction, linking to original sale_item when possible
        with transaction.atomic():
            models.create_sale_return(employee_id, sale_order_id)
            for key in cart:
                product_id = key.get('product_id')
                quantity = int(key.get('quantity'))
                unit_price = float(key.get('unit_price'))
                total_price = float(key.get('total_price'))
                original_item_id = None
                if sale_order_id:
                    orig = models.Sale_item.objects.filter(sale_order_id=sale_order_id, product_id=product_id).first()
                    if orig:
                        original_item_id = orig.id
                models.add_item_to_sale_return(product_id, quantity, unit_price, total_price, original_item_id)

            # compute grand total and save to sale return record
            try:
                grand = sum(float(item.get('total_price')) for item in cart)
            except Exception:
                grand = 0.0
            last_sr = models.SaleReturn.objects.last()
            if last_sr:
                last_sr.grand_total = grand
                last_sr.total_amount = grand
                last_sr.save()

        # clear session cart and return
        _save_sale_returns_cart(request, [])
        messages.success(request, "Sale return recorded!", extra_tags='sale_return')
        return redirect('/return_sales')


def clear_sale_returns_cart(request):
    cart = _get_sale_returns_cart(request)
    if not cart:
        messages.error(request, "already empty!")
        return redirect('/return_sales')
    else:
        # if clearing, reverse the earlier restock
        for item in cart:
            try:
                models.add_product_to_sale(item.get('product_id'), int(item.get('quantity')))
            except Exception:
                pass
        _save_sale_returns_cart(request, [])
        return redirect('/return_sales')


def view_sale_return(request, id):
    context = {
        'invoice': models.get_sale_return(id),
        'return_products': models.sale_return_products(id),
    }
    return render(request, 'view_return_sale.html', context)


def print_sale_return(request, id):
    context = {
        'invoice': models.get_sale_return(id),
        'return_products': models.sale_return_products(id),
    }
    return render(request, 'print_return_sale.html', context)


def print_return_invoice(request, id):
    # standalone printable page for the return invoice
    context = {
        'invoice': models.get_return_invoice(id),
        'return_products': models.return_invoices_products(id),
    }
    return render(request, 'print_return_invoice.html', context)


def print_sale_invoice(request, id):
    context = {
        'order': models.get_sale_order(id),
        'sale_products': models.sale_orders_products(id),
    }
    return render(request, 'print_sale_invoice.html', context)


def print_purchase_invoice(request, id):
    context = {
        'invoice': models.get_purchases(id),
        'purchase_products': models.purchase_invoices_products(id),
    }
    return render(request, 'print_purchase_invoice.html', context)

def clear_sales_list(request) :
    cart = _get_sale_cart(request)
    if not cart:
        messages.error(request, "already empty!")
        return redirect('/sales')
    _save_sale_cart(request, [])
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
    sale_qs = models.sale_orders_products(id)
    context={
        'order': models.get_sale_order(id),
        'sale_products': sale_qs,
        'sale_products_count': sale_qs.count(),
        'page_title': _("View Sale Order"),
        'no_products_message': _("No products found in this sale order."),
    }
    return render(request, 'view_sale_order.html',context)

def view_purchase_invoice(request,id):
    context={
        # 'order': models.get_sale_order(id),
        'invoice': models.get_purchases(id),
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
