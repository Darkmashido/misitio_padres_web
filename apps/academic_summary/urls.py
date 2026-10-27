from django.urls import path

from .views import AcademicSummaryView

app_name = "academic_summary"

urlpatterns = [
    path("<int:student_id>/", AcademicSummaryView.as_view(), name="detail"),
]
