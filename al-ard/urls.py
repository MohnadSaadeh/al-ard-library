from django.contrib import admin
from django.urls import path, include

# THIS SECTION IS NEW!
# ********************
from my_app.models import Manager

class ManagerAdmin(admin.ModelAdmin):
    pass
#admin.site.register(Manager, ManagerAdmin)

# ****************

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_app.urls')),
    path('i18n/', include('django.conf.urls.i18n')),

]

# Custom error handlers
handler400 = 'my_app.views.error_400'
handler403 = 'my_app.views.error_403'
handler404 = 'my_app.views.error_404'
handler500 = 'my_app.views.error_500'
