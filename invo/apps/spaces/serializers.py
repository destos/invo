from rest_framework import serializers
from . import models


class SpaceNodeSerializer(serializers.ModelSerializer):
    # parent = serializers.PrimaryKeyRelatedField(queryset=SpaceNode.objects.all(), required=False)
    # name = serializers.CharField(required=False)
    dimensions = serializers.ModelField(
        source="size", model_field=models.SpaceNode._meta.get_field("size"), required=False
    )
    # layout = serializers.ModelField(model_field=models.SpaceNode._meta.get_field('layout'))
    layout = serializers.ModelField(model_field=models.SpaceNode.layout, required=False)

    grid_scale = serializers.ModelField(
        # source="grid_scale",
        model_field=models.GridSpaceNode._meta.get_field("grid_scale"),
        required=False,
    )

    class Meta:
        model = models.SpaceNode
        fields = (
            "name",
            "parent",
            "layout",
            "dimensions",
            "grid_scale",
        )
        extra_kwargs = {"name": {"required": False}, "parent": {"required": False}}

    def validate_dimensions(self, value):
        return [value["x"], value["y"], value["z"]]


class GridSpaceNodeSerializer(SpaceNodeSerializer):
    grid_size = serializers.DictField(allow_empty=True)

    class Meta(SpaceNodeSerializer.Meta):
        model = models.GridSpaceNode
        fields = ("name", "parent", "layout", "dimensions", "grid_scale", "grid_size")
        # extra_kwargs = {"name": {"required": False}, "parent": {"required": False}}

    def validate_grid_size(self, value):
        assert isinstance(value, dict)
        return [value["cols"], value["rows"]]
