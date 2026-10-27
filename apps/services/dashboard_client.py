from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


@dataclass(frozen=True)
class FinancialStatus:
    status: str
    fecha: str | None = None


@dataclass(frozen=True)
class ChildCard:
    id: int
    nombre: str
    grado: str
    tareas: int
    examenes: int
    finanzas: FinancialStatus
    color: str
    image_url: str | None = None


def get_dashboard_children() -> list[ChildCard]:
    return [
        ChildCard(
            id=1,
            nombre="Mateo Gomez",
            grado="4to Grado",
            tareas=2,
            examenes=1,
            finanzas=FinancialStatus(status="vencida"),
            color="indigo",
            image_url="https://images.unsplash.com/photo-1519452635265-7b1fbfd1e4e0?q=80&w=150&h=150&auto=format&fit=crop",
        ),
        ChildCard(
            id=2,
            nombre="Lucia Gomez",
            grado="1er Ano",
            tareas=0,
            examenes=0,
            finanzas=FinancialStatus(status="proxima", fecha="15/03"),
            color="pink",
            image_url=None,
        ),
    ]



@dataclass(frozen=True)
class Notification:
    titulo: str
    detalle: str
    tiempo: str
    tipo: str
    leida: bool = False


@dataclass(frozen=True)
class InboxMessage:
    remitente: str
    asunto: str
    extracto: str
    tiempo: str
    leido: bool = False


def get_notifications() -> list[Notification]:
    return [
        Notification("Cuota vencida", "La cuota de Mateo Gomez esta vencida.", "Hace 1 h", "pago"),
        Notification("Nueva tarea", "Matematicas: ejercicios de la pagina 42.", "Hace 3 h", "tarea"),
        Notification("Examen proximo", "Examen de Lengua el viernes.", "Ayer", "examen"),
        Notification("Cuota proxima", "La cuota de Lucia Gomez vence el 15/03.", "Hace 2 dias", "pago", True),
    ]


def get_inbox_messages() -> list[InboxMessage]:
    return [
        InboxMessage("Prof. Ana Perez", "Reunion de padres", "Le escribo para coordinar una reunion...", "Hace 30 min"),
        InboxMessage("Secretaria", "Documentacion pendiente", "Falta entregar el certificado medico...", "Hace 5 h"),
        InboxMessage("Direccion", "Acto escolar", "Les recordamos el acto del lunes...", "Hace 3 dias", True),
    ]



@dataclass(frozen=True)
class Attendance:
    estado: str
    entrada: str | None = None


@dataclass(frozen=True)
class NextExam:
    materia: str
    fecha: str
    temario_url: str = "#"


@dataclass(frozen=True)
class PendingForm:
    titulo: str
    vencimiento: str
    url: str = "#"


@dataclass(frozen=True)
class StudentActivities:
    nombre: str
    asistencia: Attendance
    examen: NextExam | None
    formulario: PendingForm | None


_STUDENT_ACTIVITIES = {
    1: StudentActivities(
        nombre="Mateo",
        asistencia=Attendance(estado="presente", entrada="08:30 AM"),
        examen=NextExam(materia="Matematicas", fecha="Oct 24 • 10:00 AM"),
        formulario=PendingForm(titulo="Formulario Excursion", vencimiento="Vence en 2 dias"),
    ),
    2: StudentActivities(
        nombre="Lucia",
        asistencia=Attendance(estado="ausente"),
        examen=None,
        formulario=None,
    ),
}


def get_student_activities(student_id: int) -> StudentActivities | None:
    return _STUDENT_ACTIVITIES.get(student_id)



CALENDAR_CATEGORIES = {
    "examen": {"label": "Examenes", "color": "#3b82f6", "icon": "fa-file-pen"},
    "feriado": {"label": "Feriados", "color": "#f59e0b", "icon": "fa-umbrella-beach"},
    "institucional": {"label": "Institucional", "color": "#ef4444", "icon": "fa-building"},
}


@dataclass(frozen=True)
class CalendarEvent:
    id: int
    titulo: str
    categoria: str
    inicio: datetime
    alumno: str
    lugar: str | None = None
    student_id: int | None = None  # None: aplica a todos los alumnos


def _calendar_events() -> list[CalendarEvent]:
    today = date.today()

    def at(days: int, hour: int, minute: int = 0) -> datetime:
        return datetime.combine(today + timedelta(days=days), time(hour, minute))

    return [
        CalendarEvent(1, "Examen Algebra Avanzada", "examen", at(0, 9), "Mateo", "Room 402", 1),
        CalendarEvent(2, "Preparacion Dia del Maestro", "institucional", at(0, 12, 30), "Todos", "Patio central"),
        CalendarEvent(3, "Taller de Arte", "institucional", at(0, 14, 30), "Lucia", "Aula de arte", 2),
        CalendarEvent(4, "Examen de Lengua", "examen", at(3, 10), "Mateo", "Room 210", 1),
        CalendarEvent(5, "Examen de Lectura", "examen", at(5, 8, 30), "Lucia", "Aula 3", 2),
        CalendarEvent(6, "Feriado nacional", "feriado", at(9, 0), "Todos"),
    ]


def get_calendar_events(
    student_id: int,
    categories: list[str] | None = None,
    start: date | None = None,
    end: date | None = None,
) -> list[CalendarEvent]:
    events = [
        e for e in _calendar_events()
        if e.student_id in (None, student_id)
        and (not categories or e.categoria in categories)
        and (start is None or e.inicio.date() >= start)
        and (end is None or e.inicio.date() < end)
    ]
    return sorted(events, key=lambda e: e.inicio)



@dataclass(frozen=True)
class SubjectGrade:
    materia: str
    profesor: str
    p1: int
    p2: int
    final: str


@dataclass(frozen=True)
class AcademicSummary:
    nombre: str
    iniciales: str
    grado: str
    promedio: float
    promedio_variacion: float
    ranking: int
    ranking_total: int
    ranking_tendencia: str
    dias_escolares: int
    inasistencias: int
    llegadas_tarde: int
    notas: list[SubjectGrade]

    @property
    def asistencia_pct(self) -> int:
        if not self.dias_escolares:
            return 0
        return round((self.dias_escolares - self.inasistencias) / self.dias_escolares * 100)


_ACADEMIC_SUMMARIES = {
    1: AcademicSummary(
        nombre="Mateo Gomez",
        iniciales="MG",
        grado="Grado 4 • Seccion B",
        promedio=3.82,
        promedio_variacion=0.2,
        ranking=12,
        ranking_total=150,
        ranking_tendencia="Estable",
        dias_escolares=120,
        inasistencias=4,
        llegadas_tarde=2,
        notas=[
            SubjectGrade("Matematicas", "Prof. Miller", 88, 92, "A-"),
            SubjectGrade("Fisica", "Prof. Chen", 76, 74, "C+"),
            SubjectGrade("Literatura", "Prof. Adams", 95, 98, "A+"),
            SubjectGrade("Historia", "Prof. Garcia", 62, 68, "D"),
        ],
    ),
    2: AcademicSummary(
        nombre="Lucia Gomez",
        iniciales="LG",
        grado="1er Ano • Seccion A",
        promedio=3.45,
        promedio_variacion=-0.1,
        ranking=40,
        ranking_total=150,
        ranking_tendencia="Estable",
        dias_escolares=120,
        inasistencias=9,
        llegadas_tarde=5,
        notas=[
            SubjectGrade("Lengua", "Prof. Lopez", 80, 84, "B"),
            SubjectGrade("Matematicas", "Prof. Ruiz", 70, 72, "C"),
        ],
    ),
}


def get_academic_summary(student_id: int) -> AcademicSummary | None:
    return _ACADEMIC_SUMMARIES.get(student_id)


@dataclass(frozen=True)
class PaymentItem:
    id: int
    concepto: str
    alumno: str
    monto: float
    status: str
    vence: str


@dataclass(frozen=True)
class PaymentDocument:
    nombre: str
    meta: str


_PAYMENT_ITEMS = [
    PaymentItem(1, "Cuota - Octubre", "Mateo Gomez", 1200.00, "vencida", "30/09"),
    PaymentItem(2, "Laboratorio - Ciencias", "Mateo Gomez", 250.00, "proxima", "15/03"),
    PaymentItem(3, "Cuota - Marzo", "Lucia Gomez", 1000.00, "proxima", "15/03"),
]

_PAYMENT_DOCUMENTS = [
    PaymentDocument("Factura #2023-0098", "PDF • 30 Sep, 2023"),
    PaymentDocument("Recibo de pago #8821", "PDF • 25 Ago, 2023"),
]


def get_pending_payments() -> list[PaymentItem]:
    return list(_PAYMENT_ITEMS)


def get_payment_documents() -> list[PaymentDocument]:
    return list(_PAYMENT_DOCUMENTS)
