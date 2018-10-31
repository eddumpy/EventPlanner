from rest_framework.pagination import LimitOffsetPagination


class EventPagination(LimitOffsetPagination):
    default_limit = 8
    limit_query_param = 'page_size'
    max_limit = 20
