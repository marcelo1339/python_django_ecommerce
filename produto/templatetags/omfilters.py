from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_brazilian_currency(value):
    return utils.format_brazilian_currency(value)