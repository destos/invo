from ariadne_extended.resolvers import ModelResolver, ListModelMixin
from .models import Situation

from graph.types import query


class SituationResolver(ModelResolver):
    model = Situation
    queryset = Situation.objects.all()

    def active(self, info, **kwargs):
        situ = self.get_queryset().get_active(self.request.user)
        if situ is None:
            # if no active, make it
            return Situation.objects.create(user=self.request.user)
        return situ


query.set_field("activeSituation", SituationResolver.as_resolver(method="active"))
