from ariadne_extended.resolvers import Resolver, InputMixin

from haystack import connections
from haystack.constants import DEFAULT_ALIAS
from haystack.query import EmptySearchQuerySet, SearchQuerySet, SQ
from haystack.utils import get_model_ct
from haystack.utils.app_loading import haystack_get_model
from graph.types import query


class SearchResolver(InputMixin, Resolver):
    input_arg = "search"

    def search(self, info, **kwargs):
        searchqueryset = SearchQuerySet()
        search = self.get_input_data()
        text = search.get("text", "")
        # sqs = searchqueryset.auto_query(text)
        sqs = searchqueryset.filter(SQ(text__fuzzy=text))
        # if self.load_all:
        #     sqs = sqs.load_all()
        suggestions = sqs.spelling_suggestion(text)
        return sqs
        # return EmptySearchQuerySet()


query.set_field("entitySearch", SearchResolver.as_resolver(method="search"))
