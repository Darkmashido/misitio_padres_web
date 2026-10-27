from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from apps.services.dashboard_client import (
    get_dashboard_children,
    get_payment_documents,
    get_pending_payments,
    get_inbox_messages,
    get_notifications,
)

PAYMENT_METHODS = [
    {"name": "Tarjeta de crédito", "icon": "fa-credit-card", "color": "bg-blue-50 text-blue-600"},
    {"name": "Transferencia QR", "icon": "fa-qrcode", "color": "bg-purple-50 text-purple-600"},
]

STATUS_LABELS = {"vencida": "Vencido", "proxima": "Próximo"}


class PaymentsView(View):
    template_name = "payments/index.html"

    def get(self, request):
        user = request.session.get("mock_user")
        if not user:
            messages.info(request, "Inicia sesion para continuar.")
            return redirect("authentication:login")

        payments = get_pending_payments()
        notifications = get_notifications()
        inbox_messages = get_inbox_messages()
        context = {
            "mock_user": user,
            "students": get_dashboard_children(),
            "balance": sum(p.monto for p in payments),
            "next_due": next((p.vence for p in payments if p.status == "proxima"), None),
            "pending_payments": [{**p.__dict__, "label": STATUS_LABELS[p.status]} for p in payments],
            "payment_methods": PAYMENT_METHODS,
            "documents": get_payment_documents(),
            "notifications": notifications,
            "inbox_messages": inbox_messages,
            "unread_notifications": sum(not n.leida for n in notifications),
            "unread_messages": sum(not m.leido for m in inbox_messages),
        }
        return render(request, self.template_name, context)
