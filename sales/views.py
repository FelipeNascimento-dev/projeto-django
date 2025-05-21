from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer

class SaleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SaleSerializer

    def get_queryset(self):
        queryset = Sale.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        product = self.request.query_params.get('product')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if product:
            queryset = queryset.filter(product__icontains=product)
            
        return queryset