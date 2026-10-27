from django.urls import path

from .views import CalendarEventsView, CalendarView

app_name = "calendar"

urlpatterns = [
    path("", CalendarView.as_view(), name="index"),
    path("events/", CalendarEventsView.as_view(), name="events"),
]
