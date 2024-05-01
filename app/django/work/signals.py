from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save, pre_delete

from .models import (Issue, IssueRelation, IssueComment,
                     TimeEntry, ActivityLogEntry, IssueLogEntry)


@receiver(pre_save, sender=Issue)
def issue_track_changes(sender, instance, **kwargs):
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
        if old_instance.closed is None and instance.closed is not None:
            instance._old_closed = old_instance.closed


@receiver(post_save, sender=Issue)
def issue_log_changes(sender, instance, created, **kwargs):
    action = "Created" if created else "Updated"
    status_log = ""
    details = f"**업무** - *{instance}(#{instance.id})*업무가 *{action}* 되었습니다." if created else ""
    diff = ""
    parent_details = ""
    if hasattr(instance, '_old_project'):
        details += f"|- **프로젝트**가 *{instance._old_project}*에서 *{instance.project}*(으)로 변경되었습니다."
    if hasattr(instance, '_old_tracker'):
        details += f"|- **유형**이 *{instance._old_tracker}*에서 *{instance.tracker}*(으)로 변경되었습니다."
    if hasattr(instance, '_old_status'):
        status_log = instance.status.name
        details += f"|- **상태**가 *{instance._old_status}*에서 *{instance.status}*(으)로 변경되었습니다."
    if hasattr(instance, '_old_priority'):
        details += f"|- **우선순위**가 _{instance._old_priority}_ 에서 _{instance.priority}*(으)로 변경되었습니다."
    if hasattr(instance, '_old_subject'):
        details += f"|- **제목**이 *{instance._old_subject}*에서 *{instance.subject}*(으)로 변경되었습니다."
    if hasattr(instance, '_old_description'):
        details += f"|- **설명**이 변경되었습니다."
        diff += f"**변경전 :**\n{instance._old_description}\n---\n**변경후 :**\n{instance.description}"
    if hasattr(instance, '_old_category'):
        desc = f"*{instance._old_category}*에서 " if instance._old_category else ""
        act = "변경" if instance._old_category else "지정"
        details += f"|- **범주**가 {desc}*{instance.category}*(으)로 {act}되었습니다."
    if hasattr(instance, '_old_fixed_version'):
        desc = f" *{instance._old_fixed_version}*에서 " if instance._old_fixed_version else ""
        act = "변경" if instance._old_fixed_version else "지정"
        details += f"|- **목표 버전**이 {desc}*{instance.fixed_version}*(으)로 {act}되었습니다."
    if hasattr(instance, '_old_assigned_to'):
        desc = f" *{instance._old_assigned_to}*에서 " if instance._old_assigned_to else ""
        act = "변경" if instance._old_assigned_to else "지정"
        details += f"|- **담당자**가 {desc}*{instance.assigned_to}*(으)로 {act}되었습니다."
    if hasattr(instance, '_old_parent'):
        desc = f" *{instance._old_parent}*에서 " if instance._old_parent else ""
        act = "변경" if instance._old_parent else "지정"
        details += f"|- **상위 업무**가 {desc}#{instance.parent.pk} *{instance.parent}*(으)로 {act}되었습니다."
        parent_details = f"|- **하위 업무**에 #{instance.pk} *{instance}*이(가) 추가되었습니다."
    if hasattr(instance, '_old_watchers'):
        desc = f" *{instance._old_watchers}*에서 " if instance._old_watchers else ""
        act = "변경" if instance._old_watchers else "지정"
        details += f"|- **업무 열람 공유자**가 {desc}*{instance.watchers}*(으)로 {act}되었습니다."
    if hasattr(instance, '_old_is_private'):
        details += f"|- **비공개 설정**이 *{instance._old_is_private}*에서 *{instance.is_private}*(으)로 변경되었습니다."
    if hasattr(instance, '_old_estimated_hours'):
        desc = f" *{instance._old_estimated_hours}*에서 " if instance._old_estimated_hours else ""
        act = "변경" if instance._old_estimated_hours else "지정"
        details += f"|- **추정시간**이 {desc}*{instance.estimated_hours}*(으)로 {act}되었습니다."
    if hasattr(instance, '_old_start_date'):
        desc = f" *{instance._old_start_date}*에서 " if instance._old_start_date else ""
        act = "변경" if instance._old_start_date else "지정"
        details += f"|- **시작 일자**가 {desc}*{instance.start_date}*(으)로 {act}되었습니다."
    if hasattr(instance, '_old_due_date'):
        desc = f" *{instance._old_due_date}*에서 " if instance._old_due_date else ""
        act = "변경" if instance._old_due_date else "지정"
        details += f"|- **완료일**이 {desc}*{instance.due_date}*(으)로 {act}되었습니다."
    if hasattr(instance, '_old_done_ratio'):
        details += f"|- **진척도**가 *{instance._old_done_ratio}*에서 *{instance.done_ratio}*(으)로 변경되었습니다."
    if hasattr(instance, '_old_closed'):
        details += f"|- **해당 업무**가 *{instance.closed}*에 종료되었습니다."

    user = instance.creator if created else instance.updater
    if created:
        # 생성 시 activity 만 기록
        ActivityLogEntry.objects.create(sort='1', project=instance.project, issue=instance, user=user)
        ##########################################
        # 생성 사용자를 제외한, 담당자와 열람자들에게 메일 전달
        ##########################################
        subject = f'새 업무 [#{instance.pk}] - [{instance.subject}] 이(가) [{instance.assigned_to.username}]님에게 할당 되었습니다.' \
            if instance.assigned_to else f'새 업무 [#{instance.pk}] - [{instance.subject}] 이(가) 생성 되었습니다.'
        message = f'''<u>{user.username}님이 새 업무 #{instance.pk} {instance.subject}를 생성 하였습니다.</u>
        
업무 : #{instance.pk} {instance.subject}
        
담당 : {instance.assigned_to.username if instance.assigned_to else ""}
        
기한 : {instance.due_date if instance.due_date else ""}
        
설명 : 
{instance.description}
        
링크 : {settings.DOMAIN_HOST}#/work/project/redmine/issue/{instance.pk}
        '''
        addresses = []
        if instance.assigned_to and instance.assigned_to != user:  # 생성자와 담당자가 다를 경우 담당자에게 메일 전달
            addresses.append(instance.assigned_to.email)
        if instance.watchers.all():  # 열람자들에게 메일 전달
            for watcher in instance.watchers:
                addresses.append(watcher.email)
        if addresses:
            try:
                send_mail(subject, message, settings.EMAIL_DEFAULT_SENDER, addresses, fail_silently=False)
            except Exception:
                pass
    else:
        # 변경 시
        if details:
            # 변경 내용 기록이 있으면 업무 로그 기록
            IssueLogEntry.objects.create(issue=instance, action=action, details=details, diff=diff, user=user)
            if hasattr(instance, '_old_parent') and parent_details:
                IssueLogEntry.objects.create(issue=instance.parent, action=action,
                                             details=parent_details, diff=diff, user=user)
            if hasattr(instance, '_old_status'):
                # 변경 내용 기록과 상태 변경이 있으면 activity 도 기록
                ActivityLogEntry.objects.create(sort='1', project=instance.project,
                                                issue=instance, status_log=status_log, user=user)
                ################################################
                # 업데이트 사용자를 제외한 생성자, 담당자, 열람자에게 메일 전달
                ################################################
                subject = f'업무 -#{instance.pk} {instance.subject}- 의 상태가 변경 되었습니다.'
                message = f'''{user.username}님이 업무 -#{instance.pk} {instance.subject}- 상태를 변경 하였습니다.
                
                https://brdnc.co.kr/#/work/project/redmine/issue/{instance.pk}
                '''
                addresses = []
                if instance.assigned_to and instance.assigned_to != user:  # 변경자가 담당자가 아니면 담당자에게 메일 전달
                    addresses.append(instance.assigned_to.email)
                if instance.creator != user:  # 변경자와 생성자가 다르면 생성자에게 메일 전달
                    addresses.append(instance.creator)
                if instance.watchers.all():  # 열람자들에게 메일 전달
                    for watcher in instance.watchers:
                        addresses.append(watcher.email)
                if addresses:
                    try:
                        send_mail(subject, message, settings.EMAIL_DEFAULT_SENDER, addresses, fail_silently=False)
                    except Exception:
                        pass


@receiver(pre_delete, sender=Issue)
def issue_log_delete(sender, instance, **kwargs):
    try:
        issue_logs = IssueLogEntry.objects.filter(issue=instance)
        issue_logs.delete()
    except IssueLogEntry.DoesNotExist:
        pass
    try:
        act_logs = ActivityLogEntry.objects.filter(issue=instance)
        act_logs.delete()
    except ActivityLogEntry.DoesNotExist:
        pass


@receiver(post_save, sender=IssueRelation)
def issue_relation_create(sender, instance, created, **kwargs):
    details = f"|- **{instance.get_relation_type_display()}** : 에 \
    *{instance.issue_to.tracker} {instance.issue_to.pk} {instance.issue_to}*이(가) 추가되었습니다."
    if created:
        IssueLogEntry.objects.create(issue=instance.issue, action='Updated',
                                     details=details, user=instance.user)


@receiver(pre_delete, sender=IssueRelation)
def issue_relation_delete(sender, instance, **kwargs):
    details = f"|- **{instance.get_relation_type_display()}** : 값이 삭제되었습니다. \
    (*{instance.issue_to.tracker} {instance.issue_to.pk} {instance.issue_to}*)"
    IssueLogEntry.objects.create(issue=instance.issue, action='Updated',
                                 details=details, user=instance.user)


@receiver(post_save, sender=IssueComment)
def comment_log_changes(sender, instance, created, **kwargs):
    if created:
        IssueLogEntry.objects.create(issue=instance.issue, action='Comment', comment=instance, user=instance.user)
        ActivityLogEntry.objects.create(sort='2', project=instance.issue.project, issue=instance.issue,
                                        comment=instance, user=instance.user)


@receiver(pre_delete, sender=IssueComment)
def comment_log_delete(sender, instance, **kwargs):
    # 로그 삭제 or 삭제된 코멘트인지 로그 업데이트
    try:
        issue_logs = IssueLogEntry.objects.filter(comment=instance)
        issue_logs.delete()
    except IssueLogEntry.DoesNotExist:
        pass
    try:
        act_logs = ActivityLogEntry.objects.filter(comment=instance)
        act_logs.delete()
    except ActivityLogEntry.DoesNotExist:
        pass


@receiver(post_save, sender=TimeEntry)
def time_log_changes(sender, instance, created, **kwargs):
    if created:
        ActivityLogEntry.objects.create(sort='9', project=instance.issue.project, issue=instance.issue,
                                        spent_time=instance, user=instance.user)


@receiver(pre_delete, sender=TimeEntry)
def time_log_delete(sender, instance, **kwargs):
    try:
        act_logs = ActivityLogEntry.objects.filter(spent_time=instance)
        act_logs.delete()
    except ActivityLogEntry.DoesNotExist:
        pass
