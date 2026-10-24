from django.db.models import Q
from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from work.models import ActivityLogEntry, IssueLogEntry


@admin.register(ActivityLogEntry)
class ActivityLogEntryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sort', 'title', 'project', 'act_date')
    list_display_links = ('title',)
    list_select_related = ('project', 'creator')
    list_filter = ('project', 'sort', ('act_date', DateRangeFilter))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser or getattr(user, 'work_manager', False):
            return qs
        return qs.filter(Q(project__is_public=True) | Q(project__members__user=user)).distinct()


@admin.register(IssueLogEntry)
class IssueLogEntryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'action', 'issue', 'comment_id', 'details', 'diff', 'timestamp')
    list_display_links = ('issue',)
    list_select_related = ('issue', 'comment', 'creator')
    list_filter = ('action',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser or getattr(user, 'work_manager', False):
            return qs
        return qs.filter(
            Q(issue__project__is_public=True) |
            Q(issue__project__members__user=user) |
            Q(issue__creator=user) |
            Q(issue__assigned_to=user)
        ).distinct()
