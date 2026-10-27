from django.http import Http404

from apps.common.modal import ModalFragmentView
from apps.services.dashboard_client import get_student_activities


class StudentActivitiesView(ModalFragmentView):
    template_name = "student_activities/index.html"

    def get_context_data(self, request, student_id):
        activities = get_student_activities(student_id)
        if activities is None:
            raise Http404("Alumno no encontrado")
        return {"activities": activities}
