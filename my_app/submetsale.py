
# from pyexpat.errors import messages

# from django.shortcuts import redirect
# from my_app import models
# from my_app.views import _get_sale_cart, _save_sale_cart
# from django.utils.translation import gettext as _
# from django.db.models import Sum




# def submet_sale_order(request):
#     cart = _get_sale_cart(request)
#     if not cart:
#         messages.error(request, _("Please add at least one product to sale!"))
#         return redirect('/sales')
#     else:
#         employee_id = request.session['employee_id']
#         # Get payment method from form POST
#         pay_method = request.POST.get('invoice_pay_method', 'cash')
#         # Read optional customer_id from the form
#         customer_id = request.POST.get('customer_id') or None
#         if customer_id:
#             try:
#                 customer_id = int(customer_id)
#             except Exception:
#                 customer_id = None
        
#         # Get and validate currency
#         currency_id = request.POST.get('currency_id')
#         if not currency_id:
#             messages.error(request, _("Please select a currency before submitting the sale!"))
#             return redirect('/sales')
        
#         # Create sale order and set payment method, customer, and currency
#         sale_order = models.create_sale_order(employee_id, customer_id)
#         sale_order.invoice_pay_method = pay_method
#         333333333333
        
#         # Set currency and calculate exchange rate if currency is selected
#         if currency_id:
#             try:
#                 sale_order.currency_id = currency_id
#                 # Get exchange rate for selected currency to base currency
#                 from datetime import date
#                 # Get exchange rate for selected currency ()
                
#                 # means: true if you defined an exchange_rate in your ExchangeRate TABLE in your company profile from currency to curency 
#                 # means: is there an ExchangeRate from (purchased currenct to BASE_currency) ?
#                 # ----EXAMBLE----
#                 # if you didnt add in (ExchangeRate TABLE) USD to USD :
#                 # if PURCHASE_CURRENCT == USD
#                 # and BASE_CURRENCY == USD
#                 # USD to USD : exchange_rate_obj == False
#                 exchange_rate_obj = models.ExchangeRate.objects.filter(
#                     from_currency_id=currency_id,
#                     to_currency__id=models.CompanyProfile.objects.first().base_currency_id if models.CompanyProfile.objects.first() and models.CompanyProfile.objects.first().base_currency else None,
#                     date=date.today()
#                 ).first()
                
#                 # if found a record in the table (ExchangeRate)
#                 # git that rate 
#                 # put it in purchase.exchange_rate_to_base
#                 if exchange_rate_obj:
#                     sale_order.exchange_rate_to_base = exchange_rate_obj.rate
#                 elif currency_id != (models.CompanyProfile.objects.first().base_currency_id if models.CompanyProfile.objects.first() else None):
#                     # If no rate found and it's not the base currency, set rate to 1.0 as fallback
#                     sale_order.exchange_rate_to_base = 1.0
#             except Exception as e:
#                 messages.warning(request, _("Could not set exchange rate: %(err)s") % {'err': str(e)})
        
#         sale_order.save()
        

#         for key in cart:
#             product_id = key.get('product_id')
#             quantity = int(key.get('quantity'))
#             models.add_item_to_invoice(product_id, quantity)
#             models.add_product_to_sale(product_id, quantity)

#         # update the created Purchase total (grand_total and total_amount)
#         try:
            
#             last_sale = models.Sale_order.objects.last()
#             total_sum = models.Sale_item.objects.filter(sale_order=last_sale).aggregate(total=Sum('total_price'))['total'] or 0
#             last_sale.grand_total = total_sum
#             last_sale.total_amount = total_sum
            
#             #_#_#_#_#_#_#_#_# (exchange_rate_to_base)
#             # Calculate total_price_base if currency and exchange rate are set
#             if last_sale.currency_id and last_sale.exchange_rate_to_base:
#                 last_sale.total_price_base = total_sum * last_sale.exchange_rate_to_base
#                 # Also update (purchase_items) with total_price_base
#                 for item in models.Sale_item.objects.filter(sale_order_id=last_sale):
#                     item.currency_id = last_sale.currency_id
#                     item.exchange_rate_to_base = last_sale.exchange_rate_to_base
#                     item.total_price_base = item.total_price * last_sale.exchange_rate_to_base
#                     item.save()
            
#         except Exception as e:
#             pass

#         _save_sale_cart(request, [])
#         messages.success(request, _("Successfully Sold!"), extra_tags='sold_product')

#         return redirect('/sales')

# #____________________________________SALE___________________________________