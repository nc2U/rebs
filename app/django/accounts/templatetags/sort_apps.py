from django import template
from django.conf import settings

register = template.Library()


@register.filter
def sort_apps(apps):
    app_order = getattr(settings, 'APP_ORDER', [])
    count = len(apps)
    apps.sort(
        key=lambda x: app_order.index(x['app_label']) if x['app_label'] in app_order else count
    )
    return apps
