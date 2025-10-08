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
