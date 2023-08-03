from django.contrib import admin
from django.urls import path, include

from .apidocs import schema_view

urlpatterns = [
    path('', include('adminlte.urls')),
    path('admin/', admin.site.urls),
    path('v1/', include('products.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
