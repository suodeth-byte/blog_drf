from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class HomePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    # page_size_query_param = 'pg_sz'
    max_page_size = 2
    page_query_description = 'page_number'


class HomeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    limit_query_param = 'lim'
    offset_query_param = 'ofs'
    max_limit = 10
