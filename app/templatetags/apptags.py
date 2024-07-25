from django import template
from django.utils.http import urlencode
from app.models import Cities, Product_Category




register = template.Library()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)



@register.simple_tag()
def get_cities():
    return Cities.objects.all()



@register.simple_tag()
def get_product_categories():
    return Product_Category.objects.all()


@register.simple_tag()
def get_total_price(price=0, nds=0, delivery=0):
    return price + nds + delivery