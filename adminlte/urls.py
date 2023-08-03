from django.urls import path

from .views import Index, SimpleDataTable, JsGrid, DataTable

urlpatterns = [
    path('admin/', Index.as_view(), name='index'),
    path('admin/simple', SimpleDataTable.as_view(), name='simple'),
    path('admin/jsgrid', JsGrid.as_view(), name='jsgrid'),
    path('admin/data', DataTable.as_view(), name='data')
]
