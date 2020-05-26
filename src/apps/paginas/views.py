
from django.views.generic import DetailView
from .models import Pagina

# Create your views here.
class PageDetail(DetailView):
    model = Pagina
    template_name = "paginas/pagina.html"
