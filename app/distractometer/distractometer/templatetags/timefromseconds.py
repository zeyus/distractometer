import datetime
from django import template

register = template.Library()

@register.filter
def timefromseconds(seconds):
    return str(datetime.timedelta(seconds=seconds))


register.filter('timefromseconds', timefromseconds)