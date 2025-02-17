from mailcap import lookup
from django import forms
import django_filters
from django_filters import FilterSet
from .models import Post

class PostFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name = 'time_in',
        widget = forms.DateInput(attrs={'type': 'date'}),
        label = 'Позже указываемой даты', lookup_expr = 'date__gte'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact']
        }