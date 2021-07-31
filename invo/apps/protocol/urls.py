from django.urls import path

from protocol.views import ItemQRView

urlpatterns = [
    path("item/<int:pk>/", ItemQRView.as_view(), name="item_qr"),
]
