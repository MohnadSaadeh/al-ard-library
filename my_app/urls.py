
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.display_homepage),
    path('index', views.index),#dachboard
    path('logout', views.logout),
    path('emp_logout' , views.emp_logout ),
    path('employees', views.display_employees),
    path('add_employee', views.add_new_employee),
    path('employye_dashboard', views.display_employee_dashboard),
    path('add_product', views.add_new_product),
    path('sales', views.display_sales),
    path('purchases', views.display_purchases),
    path('delete_product', views.delete_product),
    
    path('add_order_to_sale', views.add_product_to_sale),
    path('add_order_to_purchase', views.add_product_to_purchase),
    
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
    path('search', views.search_results , name='search'),# ajax
    path('clear_sales_list', views.clear_sales_list),
    path('clear_purchases_list', views.clear_purchases_list),

    path('view_purchase_invoice/<int:id>', views.view_purchase_invoice),


    path('get_active_users/', views.get_active_users, name='get_active_users')


]