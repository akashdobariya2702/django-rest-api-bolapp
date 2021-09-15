import requests, base64
import json

from datetime import datetime, date, time, timedelta

from django.db import models

# Create your models here.

class CreateModifiedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ShopDetail(CreateModifiedModel):
    """all seller's credential details."""
    name = models.CharField(max_length = 50)
    client_id = models.CharField(max_length = 250)
    client_secret = models.TextField()

    def __str__(self):
        return "%s: %s" %(self.id, self.name)

    class Meta:
        app_label           = 'api'
        verbose_name        = "Shop Detail"
        verbose_name_plural = "Shop Details"


class Shipment(CreateModifiedModel):
    """all Shipments sync from apis."""
    FULFILMENT_TYPE = (
        ('FBR', 'FBR'),
        ('FBB','FBB')
    )

    shipment_id = models.PositiveIntegerField()
    shipment_date = models.DateTimeField()
    transport_id = models.PositiveIntegerField()
    basic_info = models.TextField()
    complete_info = models.TextField()
    fulfilment_method = models.CharField(choices=FULFILMENT_TYPE, max_length=10)
    shop_detail = models.ForeignKey(ShopDetail, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" %(self.id, self.shipment_id)

    class Meta:
        app_label           = 'api'
        verbose_name        = "Shipment"
        verbose_name_plural = "Shipments"

    # def __init__(self, arg):
    #     super(Shipment, self).__init__()
    #     self.arg = arg
