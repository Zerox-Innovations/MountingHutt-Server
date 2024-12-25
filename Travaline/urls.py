
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('package/',include('package.urls')),
    path('admins/',include('admins.urls')),
    path('users/',include('users.urls'))
]
