from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('adminlte.urls')),
    path('admin/', admin.site.urls),
    path('v1/', include('products.urls')),
]