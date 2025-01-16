from celery import shared_task
from datetime import datetime, timedelta
from .models import Booking
from accounts.models import CustomUser
from django.utils.timezone import now

@shared_task
def delete_pending_bookings(user_id):
    threshold_time = now() - timedelta(minutes=5)
    user = CustomUser.objects.get(id=user_id)
    pending_bookings = Booking.objects.filter(status='Pending', created_at__lte=threshold_time, user=user)
    print(pending_bookings,'pedinggggg')
    pending_bookings.delete()
    return f"Pending bookings for user {user} deleted"



from celery import Celery
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import timedelta

app = Celery('Travaline')

@app.task
def reset_periodic_task():
    # Fetch and delete the existing periodic task if it exists
    PeriodicTask.objects.filter(name='delete-pending-bookings').delete()

    # Create the interval schedule (every 5 minutes)
    interval, created = IntervalSchedule.objects.get_or_create(every=5, period=IntervalSchedule.MINUTES)

    # Create or update the periodic task to run the delete_pending_bookings task every 5 minutes
    PeriodicTask.objects.create(
        interval=interval,  # Set the interval to every 5 minutes
        name='delete-pending-bookings',
        task='package.tasks.delete_pending_bookings',  # The task to run
    )


