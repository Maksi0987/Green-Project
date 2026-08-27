from django import template

register = template.Library()

@register.filter(name='user_role')
def user_role(user_obj):
    """Повертає текстову роль користувача на основі його прав"""
    if user_obj.is_staff:
        return "Адміністратор"
    return "Користувач"