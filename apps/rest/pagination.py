from rest_framework.pagination import PageNumberPagination

class PostPageNumber(PageNumberPagination):
	page_size = 20
	