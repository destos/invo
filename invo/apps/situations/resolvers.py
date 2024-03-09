from ariadne_extended.resolvers import ListModelMixin, ModelResolver
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site

from .models import Situation
from .types import situation
from graph.types import mutation, query
from owners.resolvers import OwnerResolverMixin


class SituationResolver(OwnerResolverMixin, ModelResolver):
    model = Situation
    queryset = Situation.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(site=get_current_site(self.request))

    def get_active(self):
        user = getattr(self.request, "user", None)
        # Catch un-authed users for now
        if user is None or isinstance(user, AnonymousUser):
            return None
        situ = self.get_queryset().get_active(user)
        # No active situation found create and return a new one
        if situ is None:
            # if no active, make it
            site = get_current_site(self.request)
            return Situation.objects.create(user=user, site=site)
        return situ

    def active(self, info, **kwargs):
        active = self.get_active()
        self.check_object_permissions(self.request, active)
        return active

    def select_entities(self, info, irns=list(), **kwargs):
        active = self.get_active()
        self.check_object_permissions(self.request, active)
        entities = []
        if active is not None:
            entities = [i.get_instance() for i in irns]
            active.select(*entities)
            active.save()
            return dict(object=active, entities=entities, success=True)

        return dict(object=active, entities=entities, success=False)

    def unselect_entities(self, info, irns=list(), **kwargs):
        active = self.get_active()
        self.check_object_permissions(self.request, active)
        entities = []
        if active is not None:
            entities = [i.get_instance() for i in irns]
            active.unselect(*entities)
            active.save()
            return dict(object=active, entities=entities, success=True)

        return dict(object=active, entities=entities, success=False)


@situation.field("items")
def resolve_situation_items(situ, info, **kwargs):
    return situ.items.all()


@situation.field("spaces")
def resolve_situation_spaces(situ, info, **kwargs):
    return situ.spaces.all()


query.set_field("activeSituation", SituationResolver.as_resolver(method="active"))
mutation.set_field("selectEntities", SituationResolver.as_resolver(method="select_entities"))
mutation.set_field("unselectEntities", SituationResolver.as_resolver(method="unselect_entities"))
