from django import template

register = template.Library()

@register.filter
def currency(value):
    """
    Format a number as currency with commas.
    Example: 1200000 -> 1,200,000
    """
    try:
        value = float(value)
        return "{:,.2f}".format(value)
    except (ValueError, TypeError):
        return value
