from django_filters import rest_framework as filters
from.models import *


class JournalFilter(filters.FilterSet):
    date_gte = filters.IsoDateTimeFilter(field_name="created_at", lookup_expr='gte')
    date_lte = filters.IsoDateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Journal
        fields = ['date_gte',
                  'date_lte']
