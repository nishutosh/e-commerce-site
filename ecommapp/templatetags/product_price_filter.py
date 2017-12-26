from django import template

register = template.Library()

@register.filter
def product_price_filter(value,args):
  unit_product_price=value/args
  return unit_product_price
