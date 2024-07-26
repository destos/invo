from typing import Any, Dict, List

from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from django_htmx.http import HttpResponseLocation

from .forms import CreateItemForm
from .models import Item


class ItemListView(FormMixin, generic.ListView):
    http_method_names = ["get", "post"]
    form_class = CreateItemForm
    model = Item
    queryset = Item.objects.all()
    context_object_name = "items"

    extra_response_kwargs = dict()

    def render_to_response(
        self, context: Dict[str, Any], **response_kwargs: Dict[str, Any]
    ) -> HttpResponse:
        response_kwargs.update(self.extra_response_kwargs)
        return super().render_to_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ItemCreateView(generic.CreateView):
    model = Item
    context_object_name = "item"
    form_class = CreateItemForm

    success_url = reverse_lazy("item_list")

    # def get_template_names(self) -> List[str]:
    #     if self.request.htmx:
    #         return [self.form_partial_template_name]
    #     return super().get_template_names()

    def form_valid(self, form):
        response = super().form_valid(form)
    #     # if self.request.htmx.target:
    #         # response = ItemListView.as_view(
    #         #     template_name=f"items/item_list.html#{self.request.htmx.target}",
    #         #     # extra_response_kwargs={"swap": "outerHTML"},
    #         #     # extra_response_kwargs={"redirect_to": "/"},
    #         #     response_class=HttpResponseLocation,
    #         # )(self.request)
    #     return response

    # def form_invalid(self, form):
    #     response = super().form_invalid(form)
    #     # render the partial
    #     if self.request.htmx:
    #         # Render the form with errors
    #         html = render_to_string('path/to/your_form_template.html', {'form': form}, request=self.request)
    #         return HttpResponse(html)
    #     return response


class ItemEditView(generic.UpdateView):
    model = Item
    context_object_name = "item"
    form_class = CreateItemForm


class ItemDetailView(generic.DetailView):
    model = Item
    context_object_name = "item"
