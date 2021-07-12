from typing import ItemsView
from django.views.generic import DetailView

from items.models.item_types import Item


class ItemQRView(DetailView):
    model = Item
    template_name = "protocol/qr.html"
