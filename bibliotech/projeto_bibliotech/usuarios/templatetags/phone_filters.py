from django import template
import re

register = template.Library()

@register.filter(name='phone_format')
def phone_format(number_string):
    if not number_string:
        return "" 
    
    digits = re.sub(r'\D', '', str(number_string))

    if len(digits) == 11: 
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    elif len(digits) == 10: 
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    else:
        return number_string 