from mindfulness.settings import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param, remove_query_param


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_next_link(self):
        if not self.page.has_next():
            return None
        path = self.request.get_full_path()
        url = STAGING_URL + path
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_size_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        path = self.request.get_full_path()
        url = STAGING_URL + path
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_size_query_param)
        return replace_query_param(url, self.page_size_query_param, page_number)
