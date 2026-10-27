from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from .forms import AuthenticationForm

MOCK_USERS = {
    "admin@misitio.com": {
        "password": "admin123",
        "name": "Administrador General",
        "role": "Administrador",
    },
    "padre@misitio.com": {
        "password": "padres123",
        "name": "Maria Perez",
        "role": "Padre de familia",
    },
}


class LoginView(View):
    template_name = "authentication/login.html"

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        form = AuthenticationForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, self.get_context(form=form), status=400)

        email = form.cleaned_data["email"].lower()
        password = form.cleaned_data["password"]
        user = MOCK_USERS.get(email)

        if not user or user["password"] != password:
            messages.error(request, "Credenciales invalidas. Usa los accesos mock para ingresar.")
            return render(request, self.template_name, self.get_context(form=form), status=400)

        request.session["mock_user"] = {
            "email": email,
            "name": user["name"],
            "role": user["role"],
        }
        messages.success(request, f"Bienvenido, {user['name']}.")
        return redirect("dashboard:index")

    def get_context(self, form=None):
        return {
            "form": form or AuthenticationForm(),
            "hide_sidebar": True,
            "mock_users": [
                {"email": email, "password": data["password"], "name": data["name"], "role": data["role"]}
                for email, data in MOCK_USERS.items()
            ],
        }


class LogoutView(View):
    def post(self, request):
        request.session.pop("mock_user", None)
        messages.success(request, "Sesion cerrada correctamente.")
        return redirect("authentication:login")
