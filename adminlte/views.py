from django.shortcuts import render

from django.views.generic import TemplateView
from rest_framework.response import Response

from parsing_project.templating import InternalTemplateView

from products.models import Product
from products.serializers import ProductsSerializer

class Index(InternalTemplateView):
    template_name = 'adminlte/index.html'
    
    def get(self, request):
        return Response()

class SimpleDataTable(InternalTemplateView):
    template_name = 'adminlte/pages/tables/simple.html'
    
    def get(self, request):
        return Response()

class JsGrid(InternalTemplateView):
    template_name = 'adminlte/pages/tables/jsgrid.html'
    
    def get(self, request):
        return Response()
    
class DataTable(InternalTemplateView):
    template_name = 'adminlte/pages/tables/data.html'
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        data = {'products': serializer.data}
        return render(request, self.template_name, data)