from app.models import TimeSlot


def del_patient(timeslot_id):
    time_slot = TimeSlot.objects.get(id=timeslot_id)  
    time_slot.patient = None
    time_slot.is_booked = False  
    return time_slot.save()  
