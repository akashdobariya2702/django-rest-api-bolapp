# python library

# django library
from rest_framework import serializers

# plugin library

# project library
from api.models import *

class ShopDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopDetail
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile')



        UserProfile.objects.filter(user=user).update(**profile_data)

        setClientUserGroup(user)

        return user

    def create(self, validated_data):
        shipment_id = validated_data.get('shipment_id')

        instance = Shipment.objects.filter(shipment_id=shipment_id).last()
        if instance:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        else:
            instance = Shipment.objects.create(**validated_data)

        return instance

    class Meta:
        model = Shipment
        fields = '__all__'

class GetShipmentSerializer(serializers.ModelSerializer):
    basic_info = serializers.SerializerMethodField()
    complete_info = serializers.SerializerMethodField()

    def get_basic_info(self, obj):
        return json.loads(obj.basic_info)

    def get_complete_info(self, obj):
        return json.loads(obj.complete_info)

    class Meta:
        model = Shipment
        fields = '__all__'
