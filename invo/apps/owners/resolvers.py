from ariadne_extended.resolvers import ListModelMixin, ModelResolver
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from graph.types import mutation, query
from rest_framework.permissions import BasePermission, IsAuthenticated


class SitePermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        site = get_current_site(request)
        return request.user.sites.filter(id=site.id).exists()

    def has_object_permission(self, request, view, obj):
        # TODO: find out if we're singular of multiple sites, do something similar to the sites manager
        return request.user.sites.filter(id=obj.site.id).exists()


class OwnerResolverMixin:
    permission_classes = [IsAuthenticated & SitePermission]


class SiteResolver(ModelResolver):
    queryset = Site.objects.all()

    def current(self, info, **kwargs):
        return get_current_site(self.request)


query.set_field("currentSite", SiteResolver.as_resolver(method="current"))
