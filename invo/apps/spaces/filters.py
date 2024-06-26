import django_filters

from .models import SpaceNode


class SpaceNodeFilter(django_filters.FilterSet):
    class Meta:
        model = SpaceNode
        fields = {"level": ("exact",), "name": ("exact", "icontains")}
