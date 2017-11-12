#from django.shortcuts import render
from django.views import generic
from apps.blog import models

# Create your views here.

class BlogIndex(generic.ListView):
	queryset = models.Entrada.objects.published()
	template_name = "blog/home.html"
	paginate_by = 2

class BlogDetail(generic.DetailView):
	model = models.Entrada
	template_name = "blog/post.html"