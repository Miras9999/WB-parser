import django_filters

from core.models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte"
    )
    price_max = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte"
    )
    rating_min = django_filters.NumberFilter(
        field_name="rating", lookup_expr="gte"
    )
    reviews_min = django_filters.NumberFilter(
        field_name="reviews_count", lookup_expr="gte"
    )

    class Meta:
        model = Product
        fields = []
