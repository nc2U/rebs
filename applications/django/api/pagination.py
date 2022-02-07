from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class PageNumberPaginationForTodoList(PageNumberPagination):
    page_size = 100


class LimitOffsetPaginationWithMaxLimit(LimitOffsetPagination):
    max_limit = 30
