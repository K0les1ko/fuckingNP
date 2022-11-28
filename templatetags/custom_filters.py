from django import template


register = template.Library()


CURRENCIES_SYMBOLS = {
   'хун': '***',
   'сун': '***',
}


@register.filter()
def currency(value, code='хун'):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'