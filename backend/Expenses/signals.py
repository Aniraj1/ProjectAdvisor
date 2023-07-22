from Limit.models import Limit
from django.db.models import Sum
from django.db import models

from notifications.signals import notify
from Expenses.models import Expenses

# Define the signal
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Expenses)
def check_limit_and_send_notification(sender, instance, created, **kwargs):
    if created:
        # Get the user's overall limit
        overall_limit = Limit.objects.filter(user=instance.user).first().overall_limit

        if overall_limit:
            expenses_total = Expenses.objects.filter(user=instance.user, created_date__month=instance.created_date.month).aggregate(total=Sum('amount'))['total']
            if expenses_total is None:
                expenses_total = 0

            limit_diff = expenses_total - overall_limit
            limit_exceeded_percent = round(abs(limit_diff / overall_limit) * 100, 2) if overall_limit != 0 else 0

            if limit_exceeded_percent >= 80:
                recipient = instance.user
                verb = 'limit_exceededdddd'
                target = instance
                notify.send(instance.user, recipient=recipient, verb=verb, target=target)

