from ariadne_extended.resolvers import ListModelMixin, ModelResolver
from django.contrib.auth.models import AnonymousUser
from graph.types import query, mutation

from .models import Situation
from .types import situation


class SituationResolver(ModelResolver):
    model = Situation
    queryset = Situation.objects.all()

    def get_active(self):
        user = getattr(self.request, "user", None)
        # Catch un-authed users for now
        if user is None or isinstance(user, AnonymousUser):
            return None
        situ = self.get_queryset().get_active(user)
        # No active situation found create and return a new one
        if situ is None:
            # if no active, make it
            return Situation.objects.create(user=user)
        return situ

    def active(self, info, **kwargs):
        return self.get_active()

    def select_entities(self, into, irns=list(), **kwargs):
        active = self.get_active()
        entities = []
        if active is not None:
            entities = [i.get_instance() for i in irns]
            active.select(*entities)
            active.save()
            return dict(object=active, entities=entities, success=True)

        return dict(object=active, entities=entities, success=False)

    def unselect_entities(self, into, irns=list(), **kwargs):
        active = self.get_active()
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
