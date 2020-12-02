import datetime
from haystack import indexes
from .models import Item


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    # text = indexes.CharField(document=True, use_template=True)
    text = indexes.CharField(document=True, model_attr="name")
    irn = indexes.CharField(model_attr="irn")
    # author = indexes.CharField(model_attr='user')
    created = indexes.DateTimeField(model_attr="created")
    modified = indexes.DateTimeField(model_attr="modified")
    deleted = indexes.DateTimeField(model_attr="deleted", null=True)

    def get_model(self):
        return Item

    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated."""
    #     return self.get_model().objects.filter(modified__gte=datetime.datetime.now())
