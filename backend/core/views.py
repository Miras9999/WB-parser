from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .exceptions import WbApiError
from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer
from .wb_parser import parse_and_save_products


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


    @action(detail=False, methods=["get"])
    def parse(self, request):
        category = request.query_params.get("query")
        if not category:
            return Response(
                {"error": "category param is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            parse_and_save_products(category)
        except WbApiError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY
            )

        filtered_qs = self.filter_queryset(
            self.get_queryset().filter(name__icontains=category)
        )
        page = self.paginate_queryset(filtered_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
