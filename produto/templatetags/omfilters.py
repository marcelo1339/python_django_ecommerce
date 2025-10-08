from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_brazilian_currency(value):
    return utils.format_brazilian_currency(value)

@register.filter
def get_qtd_cart(cart):
    return utils.total_qtd_cart(cart)

@register.filter
def get_sum_products_cart(cart):
    return utils.cart_totals(cart)