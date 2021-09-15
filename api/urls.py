from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

# plugin library

# project library
from api import views

router = DefaultRouter()


router.register(r'shop-detail', views.ShopDetailViewSet)
router.register(r'shipment', views.ShipmentViewSet)

urlpatterns = [
    url(r'^sync-shipment/$', views.SyncShipment.as_view()),
    url(r'^', include((router.urls, 'api'), namespace='v1')),
]
app_name = 'api'
