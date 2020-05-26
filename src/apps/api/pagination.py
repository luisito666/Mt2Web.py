# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php


from rest_framework.pagination import PageNumberPagination

class RankinPageNumber(PageNumberPagination):
	page_size = 20