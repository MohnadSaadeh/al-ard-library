from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.display_homepage),
    path('index', views.index),#dachboard
    path('logout', views.logout),
    path('emp_logout' , views.emp_logout ),
    path('employees', views.display_employees),
    path('add_employee', views.add_new_employee),
    path('add_product', views.add_new_product),
    path('sales', views.display_sales),
    path('purchases', views.display_purchases, name='display_purchases'),
    path('return_purchases', views.display_returns),
    path('return_sales', views.display_sale_returns),
    path('sales/<int:sale_order_id>/return/', views.sale_return_create_view, name='sale_return_create'),#sale return
    path('sales/returns/<int:id>/', views.sale_return_detail_view, name='sale_return_detail'),
    path('purchases/<int:purchase_id>/return/', views.purchase_return_create_view, name='purchase_return_create'),
    path('purchases/returns/<int:id>/', views.purchase_return_detail_view, name='purchase_return_detail'),
    path('add_order_to_return', views.add_product_to_return),
    path('add_order_to_sale_return', views.add_product_to_sale_return),
    path('submet_return_order', views.submet_return_order),
    path('submit_sale_return', views.submit_sale_return),
    path('clear_sale_returns_cart', views.clear_sale_returns_cart),
    path('clear_returns_list', views.clear_returns_list),
    path('view_return_invoice/<int:id>', views.view_return_invoice),
    path('view_return_sale/<int:id>', views.view_sale_return),
    path('print_return_invoice/<int:id>', views.print_return_invoice),
    path('print_return_sale/<int:id>', views.print_sale_return),
    path('print_sale_invoice/<int:id>', views.print_sale_invoice),
    path('print_purchase_invoice/<int:id>', views.print_purchase_invoice),
    path('print_stock_out_voucher/<int:id>', views.print_stock_out_voucher, name='print_stock_out_voucher'),
    path('delete_product', views.delete_product),
    
    path('add_order_to_sale', views.add_product_to_sale),
    path('add_order_to_purchase', views.add_product_to_purchase),
    path('scan/add-to-sale/', views.scan_add_to_sale, name='scan_add_to_sale'),
    path('scan/add-to-purchase/', views.scan_add_to_purchase, name='scan_add_to_purchase'),
    
    path('submet_sale_order', views.submet_sale_order),
    path('submet_purchase_order', views.submet_purchase_order),
    path('employee_reports', views.display_employee_reports),
    
    path('view_sale_order/<int:id>', views.view_sale_order),#--------------------------------------------Mai
    path('edit_product/<int:id>',views.display_edit_form),
    path('update_product/<int:id>', views.update_product),
    path('stock_manager',views.display_stock_for_manager),#--------------------------------------------Mai

    path('signup', views.sign_up),

    path('signin', views.sign_in),

    path('about_us', views.about_us),
    path('change_password', views.change_password),
    path('company_profile', views.display_company_profile),
    path('search', views.search_results , name='search'),# ajax
    path('clear_sales_list', views.clear_sales_list),
    path('clear_purchases_list', views.clear_purchases_list),
    path('delete-product-from-purchase', views.delete_product_from_purchase, name='delete_product_from_purchase'),
    path('update_purchase_cart', views.update_purchase_cart, name='update_purchase_cart'),
    path('delete-product-from-sale', views.delete_product_from_sale, name='delete_product_from_sale'),
    path('update_sales_cart', views.update_sales_cart, name='update_sales_cart'),

    path('view_purchase_invoice/<int:id>', views.view_purchase_invoice),
    path('add_product_to_sale_cart_by_isbn', views.add_product_to_sale_cart_by_isbn, name='add_product_to_sale_cart_by_isbn'),


    path('get_active_users/', views.get_active_users, name='get_active_users'),



    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('stock_products_report/', views.stock_products_report, name='stock_products_report'),
    path('empty_products_report/', views.empty_products_report, name='empty_products_report'),
    path('sales_products_report/', views.sales_products_report, name='sales_products_report'),
    # Suppliers
    path('suppliers', views.display_suppliers, name='suppliers_list'),
    path('suppliers/create', views.add_supplier, name='suppliers_create'),
    path('suppliers/<int:id>/edit', views.edit_supplier, name='suppliers_edit'),
    path('suppliers/<int:id>/delete', views.delete_supplier, name='suppliers_delete'),
    path('suppliers/<int:id>/', views.supplier_detail, name='supplier_detail'),
    # Customers (mirror suppliers)
    path('customers', views.display_customers, name='customers_list'),
    path('customers/create', views.add_customer, name='customers_create'),
    path('customers/<int:id>/edit', views.edit_customer, name='customers_edit'),
    path('customers/<int:id>/delete', views.delete_customer, name='customers_delete'),
    path('customers/<int:id>/', views.customer_detail, name='customer_detail'),
    
    # Excel Import/Export
    path('products/import/', views.import_products_excel, name='import_products_excel'),
    path('products/sample-excel/', views.download_sample_excel, name='download_sample_excel'),
    path('stock-products/excel/', views.download_stock_products_excel, name='download_stock_products_excel'),
    path('empty-products/excel/', views.download_empty_products_excel, name='download_empty_products_excel'),
    path('sales-products/excel/', views.download_sales_products_report_excel, name='download_sales_products_report_excel'),
    path('purchases/import/', views.import_purchase_invoices_excel, name='import_purchase_invoices_excel'),
    path('purchases/sample-excel/', views.download_sample_purchase_excel, name='download_sample_purchase_excel'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('reset_password/<str:token>', views.reset_password, name='reset_password'),
    
    path('stock_out_voucher', views.display_Stock_Out_voucher, name='display_Stock_Out_voucher'),
    # Stock Out Voucher actions
    path('add_order_to_stock_out', views.add_product_to_stock_out, name='add_order_to_stock_out'),
    path('delete-product-from-stock-out', views.delete_product_from_stock_out, name='delete_product_from_stock_out'),
    ## update cart session
    path('update_stock_out_cart', views.update_stock_out_cart, name='update_stock_out_cart'),
    ## end update cart session
    path('submit_stock_out_order', views.submit_stock_out_order, name='submit_stock_out_order'),
    path('view_stock_out_invoice/<int:id>', views.view_stock_out_invoice, name='view_stock_out_invoice'),
    path('stock_out_invoice/<int:id>/edit', views.stock_out_invoice_edit, name='stock_out_invoice_edit'),
    path('stock_out_invoice/<int:id>/add_item', views.stock_out_invoice_add_item, name='stock_out_invoice_add_item'),
    path('stock_out_invoice/<int:id>/delete_item', views.stock_out_invoice_delete_item, name='stock_out_invoice_delete_item'),
    path('stock_out_invoice/<int:id>/update_items', views.stock_out_invoice_update_items, name='stock_out_invoice_update_items'),
    path('stock_out_invoice/<int:id>/convert-to-sale', views.convert_stock_out_to_sale, name='convert_stock_out_to_sale'),
]