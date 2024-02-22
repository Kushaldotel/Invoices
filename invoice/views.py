from rest_framework import generics
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer
from rest_framework import status
from rest_framework.response import Response

class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        details_data = data.pop('details', [])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        invoice = serializer.instance
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceDetailListCreateView(generics.ListCreateAPIView):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer

class InvoiceDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer
