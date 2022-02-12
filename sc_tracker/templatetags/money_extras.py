from django import template
import locale

register = template.Library()

# this is just temporary, support multi currencies properly at some point
@register.filter
def money(value):
    return locale.currency(value, grouping=True)
