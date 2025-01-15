from celery import shared_task
from datetime import datetime, timedelta
from .models import Booking
from django.utils.timezone import now

@shared_task
def delete_pending_bookings():
    threshold_time = now() - timedelta(minutes=1)
    pending_bookings = Booking.objects.filter(status='Pending', created_at__lt=threshold_time)
    pending_bookings.delete()
    return "Data deleted"




from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import Celery
from .tasks import delete_pending_bookings

app = Celery('your_project_name')

@app.task
def reset_periodic_task():
    
    PeriodicTask.objects.filter(name='delete-pending-bookings').delete()
    
    # Now schedule the task again
    app.conf.beat_schedule['delete-pending-bookings'] = {
        'task': 'your_project_name.tasks.delete_pending_bookings',
        'schedule': IntervalSchedule(minute='*/1'),  # runs every 5 minutes
    }


