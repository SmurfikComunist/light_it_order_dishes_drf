from django_filters.rest_framework import FilterSet, DateTimeFilter


class DishDateTimeFilter(FilterSet):
    start_date = DateTimeFilter(field_name="created_at", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="created_at", lookup_expr="lte")
