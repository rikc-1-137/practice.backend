class Appointment:
    def __init__(self, appointment_id: int, client_name: str,
                 master_id: int, service_id: int, time: str):
        self.id = appointment_id
        self.client_name = client_name
        self.master_id = master_id
        self.service_id = service_id
        self.time = time

    def __repr__(self):
        return (f"Appointment(id={self.id}, client_name='{self.client_name}', "
                f"master_id={self.master_id}, service_id={self.service_id}, "
                f"time='{self.time}')")



class Master:
    def __init__(self, master_id: int, name: str):
        self.master_id = master_id
        self.name = name


class Service:
    def __init__(self, service_id: int, title: str):
        self.service_id = service_id
        self.title = title


MASTERS = {1: Master(1, "Мастер 1")}
SERVICES = {1: Service(1, "Стрижка")}


def get_master(master_id: int) -> Master | None:
    return MASTERS.get(master_id)


def get_service(service_id: int) -> Service | None:
    return SERVICES.get(service_id)



WORK_START = "08:00"
WORK_END = "20:00"


def is_working_hours(time: str) -> bool:
    """Проверяет, что время в формате 'ЧЧ:ММ' попадает в интервал 08:00–20:00."""
    try:
        hours, minutes = map(int, time.split(":"))
    except (ValueError, AttributeError):
        return False

    if not (0 <= hours < 24 and 0 <= minutes < 60):
        return False

    total_minutes = hours * 60 + minutes
    start_minutes = 8 * 60       # 08:00
    end_minutes = 20 * 60        # 20:00
    return start_minutes <= total_minutes <= end_minutes



appointments = []


def create_appointment(client_name: str,
                       master_id: int,
                       service_id: int,
                       time: str,
                       ) -> Appointment | None:
    if not client_name or not time or master_id is None or service_id is None:
        return None

    if not is_working_hours(time):
        return None

    master = get_master(master_id)
    service = get_service(service_id)

    if master is None or service is None:
        return None

    appointment = Appointment(
        appointment_id=len(appointments) + 1,
        client_name=client_name,
        master_id=master.master_id,
        service_id=service.service_id,
        time=time,
    )
    appointments.append(appointment)
    return appointment


first_appointment = create_appointment("Иванова А.А.", 1, 1, '10:00')
second_appointment = create_appointment("Петрова А.А.", 1, 1, '11:00')

print("Список записей:")
for appointment in appointments:
    print(appointment.client_name, appointment.time)

no_correct_appointment = create_appointment("Сидорова А.А.", 1, 1, '00:00')
print(len(appointments))