from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from apps.services.dashboard_client import (
    get_academic_summary,
    get_inbox_messages,
    get_notifications,
)


class AcademicSummaryView(View):
    template_name = "academic_summary/index.html"

    def get(self, request, student_id):
        user = request.session.get("mock_user")
        if not user:
            messages.info(request, "Inicia sesion para continuar.")
            return redirect("authentication:login")

        summary = get_academic_summary(student_id)
        if summary is None:
            raise Http404("Alumno no encontrado")

        notifications = get_notifications()
        inbox_messages = get_inbox_messages()
        context = {
            "mock_user": user,
            "summary": summary,
            "notifications": notifications,
            "inbox_messages": inbox_messages,
            "unread_notifications": sum(not n.leida for n in notifications),
            "unread_messages": sum(not m.leido for m in inbox_messages),
        }
        return render(request, self.template_name, context)
