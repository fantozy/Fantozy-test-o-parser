from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer


class InternalTemplateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    
    