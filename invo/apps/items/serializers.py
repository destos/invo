from rest_framework.serializers import ModelSerializer
from . import models


class ItemSerializer(ModelSerializer):
    class Meta:
        model = models.Item
        fields = ("name",)


class ToolSerializer(ModelSerializer):
    class Meta:
        model = models.Tool
        fields = ("name",)


class ConsumableSerializer(ModelSerializer):
    class Meta:
        model = models.Consumable
        fields = ("name", "count", "warning_enabled", "warning_count")
