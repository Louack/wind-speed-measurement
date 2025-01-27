from django_filters.rest_framework import FilterSet, filters

from .models import Tag


class AnemometerFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    tag = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), to_field_name="name", field_name="tags__name"
    )


class WindReadingFilterSet(FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name="name",
        field_name="anemometer__tags__name",
    )
