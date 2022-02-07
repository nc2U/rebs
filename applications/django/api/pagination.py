from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class PageNumberPaginationCustomBasic(PageNumberPagination):
    max_page_size = 100


class PageNumberPaginationForTodoList(PageNumberPagination):
    page_size = 20


class LimitOffsetPaginationWithMaxLimit(LimitOffsetPagination):
    max_limit = 30
