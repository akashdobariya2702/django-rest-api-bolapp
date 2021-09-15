# python library

# django library
from rest_framework import serializers, generics, permissions, viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from rest_framework.response import Response

# plugin library

# project library
from api.serializers import *
from api.functions import *

class ShopDetailViewSet(viewsets.ModelViewSet):
    queryset = ShopDetail.objects.all().order_by('-id')
    serializer_class = ShopDetailSerializer

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all().order_by('-id')
    serializer_class = ShipmentSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ('GET'):
            serializer_class = GetShipmentSerializer

        return serializer_class

class SyncShipment(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        # data = request.data
        # sync_shipment_data()
        r = sync_shipment_data.apply_async((), expires=datetime.now() + timedelta(days=2))
        print("SyncShipment r = %s" % (str(r)))

        return Response({"success": "notification sent successfully"})
