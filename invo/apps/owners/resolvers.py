from ariadne_extended.resolvers import ListModelMixin, ModelResolver
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import FieldDoesNotExist
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import SingularSite
from accounts.types import user
from graph.types import mutation, query


def get_site(request):
    return request.site if hasattr(request, "site") else get_current_site(request)


class SitePermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        site = get_site(request)
        return request.user.sites.filter(id=site.id).exists()

    def has_object_permission(self, request, view, obj):
        # TODO: find out if we're singular of multiple sites, do something similar to the sites manager
        return request.user.sites.filter(id=obj.site.id).exists()


# TODO: convert/add resolver mixin for current site lookup restriction. what is the most fault tollerant to prevent data leakage?
class OwnerResolverMixin:
    permission_classes = [IsAuthenticated & SitePermission]
    __field_name = None

    def get_queryset(self):
        site = get_site(self.request)
        return super().get_queryset().filter(**{self._get_field_name() + "__id": site.id})

    def _get_field_name(self):
        """ Return self.__field_name or 'site' or 'sites'. """

        if self.__field_name is None:
            try:
                self.model._meta.get_field("site")
            except FieldDoesNotExist:
                self.__field_name = "sites"
            else:
                self.__field_name = "site"
        return self.__field_name

    def perform_create(self, serializer):
        # model = self.get_model()
        model = self.model
        if issubclass(model, SingularSite):
            return serializer.save(site=get_current_site(self.request))
        else:
            site = get_current_site(self.request)
            instance = serializer.save()
            instance.sites.add(site)
            return instance


class SiteResolver(ModelResolver):
    """Resolve related sites or current site"""

    queryset = Site.objects.all()

    def current(self, info, **kwargs):
        return get_current_site(self.request)

    def sites_for_object(self, info, **kwargs):
        # TODO: is this something we solved already with the nested resolvers?
        return self.parent.sites.all()

    def site_for_object(self, info, **kwargs):
        return self.parent.site


query.set_field("currentSite", SiteResolver.as_resolver(method="current"))
user.set_field("sites", SiteResolver.as_resolver(method="sites_for_object"))
