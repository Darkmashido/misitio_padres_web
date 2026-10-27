from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class ModalFragmentView(View):
    """Base para vistas que devuelven el HTML interno de un modal.

    Las subclases definen `template_name` y `get_context_data`; el modal
    generico (`partials/modal.html`) se encarga de pedirlo e insertarlo.
    """

    template_name: str | None = None

    def get_context_data(self, request, *args, **kwargs) -> dict:
        return {}

    def get(self, request, *args, **kwargs):
        if not request.session.get("mock_user"):
            return HttpResponse(status=401)
        context = self.get_context_data(request, *args, **kwargs)
        return render(request, self.template_name, context)
