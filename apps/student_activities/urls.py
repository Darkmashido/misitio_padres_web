from django.urls import path

from .views import StudentActivitiesView

app_name = "student_activities"

urlpatterns = [
    path("<int:student_id>/", StudentActivitiesView.as_view(), name="detail"),
]
