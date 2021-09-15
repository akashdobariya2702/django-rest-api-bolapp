from django.contrib import admin

from api.models import *

class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'modified_at')
    list_filter = ('created_at', 'modified_at')
    readonly_fields = ('created_at', 'modified_at')

    list_per_page = 50
    show_full_result_count = False

class ShopDetailAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'client_id', 'created_at', 'modified_at')
    search_fields = ('id', 'name', 'client_id', )

admin.site.register(ShopDetail, ShopDetailAdmin)

class ShipmentAdmin(BaseModelAdmin):
    list_display = ('id', 'shipment_id', 'shipment_date', 'transport_id', 'shop_detail', 'fulfilment_method', 'created_at', 'modified_at')
    search_fields = ('id', 'shipment_id', 'transport_id', 'fulfilment_method', 'shop_detail__name')
    list_filter = ('fulfilment_method', 'created_at', 'modified_at')
    raw_id_fields = ('shop_detail', )

    def get_queryset(self, request):
        return super(ShipmentAdmin, self).get_queryset(request).select_related('shop_detail')

admin.site.register(Shipment, ShipmentAdmin)
