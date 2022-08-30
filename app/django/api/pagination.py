from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class PageNumberPaginationCustomBasic(PageNumberPagination):
    max_page_size = 5000


class LimitOffsetPaginationCustomBasic(LimitOffsetPagination):
    max_limit = 500


class PageNumberPaginationThreeThousand(PageNumberPagination):
    page_size = 3000


class PageNumberPaginationFiveHundred(PageNumberPagination):
    page_size = 500


class PageNumberPaginationThreeHundred(PageNumberPagination):
    page_size = 300


class PageNumberPaginationTwoHundred(PageNumberPagination):
    page_size = 200


class PageNumberPaginationOneHundred(PageNumberPagination):
    page_size = 100


class PageNumberPaginationFifty(PageNumberPagination):
    page_size = 50


class PageNumberPaginationTwenty(PageNumberPagination):
    page_size = 20


class PageNumberPaginationFifteen(PageNumberPagination):
    page_size = 15


class PageNumberPaginationTen(PageNumberPagination):
    page_size = 10
