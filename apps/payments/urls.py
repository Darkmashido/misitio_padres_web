from django.urls import path

from .views import PaymentsView

app_name = "payments"

urlpatterns = [
    path("", PaymentsView.as_view(), name="index"),
]
