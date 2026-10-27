from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from apps.services.dashboard_client import (
    get_dashboard_children,
    get_inbox_messages,
    get_notifications,
)


class DashboardView(View):
    template_name = "dashboard/index.html"

    def get(self, request):
        user = request.session.get("mock_user")
        if not user:
            messages.info(request, "Inicia sesion para continuar.")
            return redirect("authentication:login")

        notifications = get_notifications()
        inbox_messages = get_inbox_messages()
        context = {
            "unread_notifications": sum(not n.leida for n in notifications),
            "unread_messages": sum(not m.leido for m in inbox_messages),
            "mock_user": user,
            "children_cards": get_dashboard_children(),
            "notifications": notifications,
            "inbox_messages": inbox_messages,
        }
        return render(request, self.template_name, context)


