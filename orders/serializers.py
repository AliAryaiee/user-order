from rest_framework import serializers

from . import models


class OrderSerializer(serializers.ModelSerializer):
    """
        Order Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = models.Order
        fields = "__all__"
