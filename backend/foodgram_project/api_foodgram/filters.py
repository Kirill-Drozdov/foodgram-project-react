from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author')
    tags = filters.CharFilter(field_name='tags__slug')
    # name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    # year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
