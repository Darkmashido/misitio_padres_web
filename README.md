# Mi Sitio Padres

Portal web para padres y tutores desarrollado con **Django** y **Tailwind CSS**. Permite consultar de forma centralizada la información de los hijos: agenda, resumen académico, actividades y pagos.

## Módulos

| Módulo | Ruta | Descripción |
|---|---|---|
| Authentication | `/` | Inicio y cierre de sesión |
| Dashboard | `/dashboard/` | Vista general de los hijos (tareas, exámenes, estado financiero) |
| Calendar | `/calendar/` | Agenda con FullCalendar, filtros por alumno y categoría |
| Academic Summary | `/academic-summary/` | Resumen académico por alumno |
| Student Activities | `/student-activities/<id>/` | Asistencia, próximos exámenes y formularios (modal) |
| Payments | `/payments/` | Saldo familiar, pagos pendientes, métodos de pago y documentos |

## Estructura

```
apps/        Módulos Django (views, urls, apps)
  services/  dashboard_client.py: datos de ejemplo (mock) de Mateo y Lucia
config/      Configuración del proyecto
templates/   Vistas HTML y partials (sidebar, topbar, modal)
theme/       App de Tailwind (estilos y comando runserver personalizado)
```

## Requisitos

- Python 3.14
- Conexión a internet la primera vez (se descarga el binario de Tailwind)

## Instalación

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz con las variables que use `config/settings.py` (por ejemplo `SECRET_KEY`).

## Ejecución

```bash
python manage.py runserver
```

Con `DEBUG=True`, este comando levanta Django **y** el watcher de Tailwind (`tailwind start`) a la vez, sin pasos adicionales. Esto lo hace el comando personalizado `theme/management/commands/runserver.py`.

La app queda disponible en http://127.0.0.1:8000/.

## Tailwind CSS

El proyecto usa [django-tailwind](https://github.com/timonweb/django-tailwind). Tailwind es un compilador: genera `theme/static/css/dist/styles.css` con las clases que aparecen en los templates.

- **Desarrollo:** `python manage.py runserver` (compila automáticamente).
- **Producción:** `DEBUG=False` no inicia el watcher. Compila antes del despliegue:
  ```bash
  python manage.py tailwind build
  python manage.py collectstatic
  ```

> `python manage.py tailwind dev` no está soportado en Windows, por eso se sobrescribe `runserver`.

## Datos

Por ahora los datos provienen de `apps/services/dashboard_client.py` (datos de ejemplo). Para conectar una API real, basta con reemplazar las funciones de ese archivo (`get_dashboard_children`, `get_pending_payments`, etc.).

## Notas sobre Payments

- Los pagos (`PaymentItem`) y documentos (`PaymentDocument`) se obtienen de `dashboard_client.py`.
- El saldo total es la suma de los montos pendientes.
- Los botones "Pagar ahora", "Ver plan", "Detalles" y descargar aún no tienen funcionalidad.
