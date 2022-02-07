from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class PageNumberPaginationCustomBasic(PageNumberPagination):
    max_page_size = 100


class LimitOffsetPaginationCustomBasic(LimitOffsetPagination):
    max_limit = 100


class PageNumberPaginationForTodoList(PageNumberPagination):
    page_size = 50
