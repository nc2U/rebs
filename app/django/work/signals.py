from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Issue, IssueLogEntry


@receiver(pre_save, sender=Issue)
def track_changes(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance has already been saved
        # Compare fields to track changes
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.project != instance.project:
            instance._old_project = old_instance.project
        if old_instance.tracker != instance.tracker:
            instance._old_tracker = old_instance.tracker
        if old_instance.status != instance.status:
            instance._old_status = old_instance.status
        if old_instance.priority != instance.priority:
            instance._old_priority = old_instance.priority
        if old_instance.subject != instance.subject:
            instance._old_subject = old_instance.subject
        if old_instance.description != instance.description:
            instance._old_description = old_instance.description
        if old_instance.category != instance.category:
            instance._old_category = old_instance.category
        if old_instance.fixed_version != instance.fixed_version:
            instance._old_fixed_version = old_instance.fixed_version
        if old_instance.assigned_to != instance.assigned_to:
            instance._old_assigned_to = old_instance.assigned_to
        if old_instance.parent != instance.parent:
            instance._old_parent = old_instance.parent
        if old_instance.watchers != instance.watchers:
            instance._old_watchers = old_instance.watchers
        if old_instance.is_private != instance.is_private:
            instance._old_is_private = old_instance.is_private
        if old_instance.estimated_hours != instance.estimated_hours:
            instance._old_estimated_hours = old_instance.estimated_hours
        if old_instance.start_date != instance.start_date:
            instance._old_start_date = old_instance.start_date
        if old_instance.due_date != instance.due_date:
            instance._old_due_date = old_instance.due_date
        if old_instance.done_ratio != instance.done_ratio:
            instance._old_done_ratio = old_instance.done_ratio
        if old_instance.closed != instance.closed:
            instance._old_closed = old_instance.closed


@receiver(post_save, sender=Issue)
def log_changes(sender, instance, created, **kwargs):
    action = 'Created' if created else 'Edited'
    details = f"- **업무** - _{instance}(#{instance.id})_ 업무가 _{action}_ 되었습니다.  " if created else ""
    diff = ""
    if hasattr(instance, '_old_project'):
        details += f"- **프로젝트**가 _{instance._old_project}_에서 _{instance.project}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_tracker'):
        details += f"- **유형**이 _{instance._old_tracker}_에서 _{instance.tracker}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_status'):
        details += f"- **상태**가 _{instance._old_status}_에서 _{instance.status}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_priority'):
        details += f"- **우선순위**가 _{instance._old_priority}_에서 _{instance.priority}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_subject'):
        details += f"- **제목**을 _{instance._old_subject}_에서 _{instance.subject}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_description'):
        details += f"- **설명**이 변경되었습니다.  "
        diff += f"_{instance._old_description}_에서 _{instance.description}_(으)로"
    if hasattr(instance, '_old_category'):
        details += f"- **범주**가 _{instance._old_category}_에서 _{instance.category}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_fixed_version'):
        details += f"- **목표 버전**이 _{instance._old_fixed_version}_에서 _{instance.fixed_version}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_assigned_to'):
        details += f"- **담당자**가 _{instance._old_assigned_to}_에서 _{instance.assigned_to}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_parent'):
        details += f"- **상위 업무**가 _{instance._old_parent}_에서 _{instance.parent}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_watchers'):
        details += f"- **업무 공유 열람**가 _{instance._old_watchers}_에서 _{instance.watchers}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_is_private'):
        details += f"- **비공개 설정**이 _{instance._old_is_private}_에서 _{instance.is_private}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_estimated_hours'):
        details += f"- **추정 소요시간**이 _{instance._old_estimated_hours}_에서 _{instance.estimated_hours}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_start_date'):
        details += f"- **시작 일자**가 _{instance._old_start_date}_에서 _{instance.start_date}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_due_date'):
        details += f"- **완료 기한**이 _{instance._old_due_date}_에서 _{instance.due_date}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_done_ratio'):
        details += f"- **진척도**가 _{instance._old_done_ratio}_에서 _{instance.done_ratio}_(으)로 변경되었습니다.  "
    if hasattr(instance, '_old_closed'):
        details += f"- **완료 여부**가 _{instance._old_closed}_에서 _{instance.closed}_(으)로 변경되었습니다.  "

    user = instance.creator if created else instance.updater
    IssueLogEntry.objects.create(issue=instance, action=action, details=details, diff=diff, user=user)
