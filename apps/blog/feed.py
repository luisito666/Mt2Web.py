from django.contrib.syndication.views import Feed 
from apps.blog.models import Entrada

class UltimosPost(Feed):
	titulo = "Blog"
	link = "/feed/"
	description = "Post Recientes"

	def items(self):
		return Entrada.objects.published()[:5]
