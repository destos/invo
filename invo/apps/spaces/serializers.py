from rest_framework import serializers
from . import models
from spaces.models import SpaceNode


class SpaceNodeSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=SpaceNode.objects.all(), required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = models.SpaceNode
        fields = ("name", "parent", "layout", "dimensions")
