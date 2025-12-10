# services/templatetags/feedback_extras.py
from django import template

register = template.Library()

@register.filter
def star_range(value):
    try:
        return range(int(value))
    except:
        return range(0)
