from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Issue, IssueLogEntry


@receiver(post_save, sender=Issue)
def log_changes(sender, instance, created, **kwargs):
    action = 'Created' if created else 'Edited'
    details = f"{action} action occurred on {sender.__name__} with ID {instance.id}"
    IssueLogEntry.objects.create(issue=instance.issue, action=action, user=instance.user, details=details)
