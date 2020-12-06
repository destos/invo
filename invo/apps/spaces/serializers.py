from rest_framework import serializers
from . import models
from spaces.models import SpaceNode


class SpaceNodeSerializer(serializers.ModelSerializer):
    # parent = serializers.PrimaryKeyRelatedField(queryset=SpaceNode.objects.all(), required=False)
    # name = serializers.CharField(required=False)
    dimensions = serializers.ModelField(
        source="size", model_field=models.SpaceNode._meta.get_field("size"), required=False
    )
    # layout = serializers.ModelField(model_field=models.SpaceNode._meta.get_field('layout'))
    layout = serializers.ModelField(model_field=models.SpaceNode.layout, required=False)

    class Meta:
        model = models.SpaceNode
        fields = ("name", "parent", "layout", "dimensions")
        extra_kwargs = {"name": {"required": False}, "parent": {"required": False}}

    def validate_dimensions(self, value):
        return [value["x"], value["y"], value["z"]]
