from django.urls import path

from . import views

urlpatterns = [
    path("", views.ItemListView.as_view(), name="item_list"),
    path("list/<int:pk>/", views.ItemDetailView.as_view(), name="item_list_detail"),
    path("list/<int:pk>/edit/", views.ItemEditView.as_view(), name="item_list_edit"),
    path("create/", views.ItemCreateView.as_view(), name="item_create"),
    path("<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("<int:pk>/edit/", views.ItemEditView.as_view(), name="item_edit"),
]
