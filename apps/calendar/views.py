from datetime import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.services.dashboard_client import (
    CALENDAR_CATEGORIES,
    get_calendar_events,
    get_dashboard_children,
    get_inbox_messages,
    get_notifications,
)


def _parse_date(value):
    try:
        return datetime.fromisoformat(value[:10]).date() if value else None
    except ValueError:
        return None


class CalendarView(View):
    template_name = "calendar/index.html"

    def get(self, request):
        user = request.session.get("mock_user")
        if not user:
            messages.info(request, "Inicia sesion para continuar.")
            return redirect("authentication:login")

        notifications = get_notifications()
        inbox_messages = get_inbox_messages()
        context = {
            "mock_user": user,
            "students": get_dashboard_children(),
            "categories": CALENDAR_CATEGORIES,
            "notifications": notifications,
            "inbox_messages": inbox_messages,
            "unread_notifications": sum(not n.leida for n in notifications),
            "unread_messages": sum(not m.leido for m in inbox_messages),
        }
        return render(request, self.template_name, context)


class CalendarEventsView(View):
    def get(self, request):
        if not request.session.get("mock_user"):
            return JsonResponse({"error": "unauthorized"}, status=401)

        try:
            student_id = int(request.GET.get("student", ""))
        except ValueError:
            return JsonResponse({"error": "student requerido"}, status=400)

        categories = [c for c in request.GET.get("types", "").split(",") if c]
        events = get_calendar_events(
            student_id,
            categories=categories or None,
            start=_parse_date(request.GET.get("start")),
            end=_parse_date(request.GET.get("end")),
        )
        return JsonResponse(
            [
                {
                    "id": e.id,
                    "title": e.titulo,
                    "start": e.inicio.isoformat(),
                    "color": CALENDAR_CATEGORIES[e.categoria]["color"],
                    "extendedProps": {
                        "categoria": e.categoria,
                        "lugar": e.lugar,
                        "alumno": e.alumno,
                    },
                }
                for e in events
            ],
            safe=False,
        )
