from rest_framework import serializers
from . import models
from spaces.models import SpaceNode


class ItemSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=SpaceNode.objects.all(), source="space")

    class Meta:
        model = models.Item
        fields = ("name", "space_id")


class ToolSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=SpaceNode.objects.all(), source="space")

    class Meta:
        model = models.Tool
        fields = ("name", "space_id")


class ConsumableSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=SpaceNode.objects.all(), source="space")

    class Meta:
        model = models.Consumable
        fields = ("name", "space_id", "count", "warning_enabled", "warning_count")
