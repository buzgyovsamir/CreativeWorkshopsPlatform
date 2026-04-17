from django import template

register = template.Library()


@register.filter
def is_organizer(user):
    return user.is_authenticated and user.groups.filter(name='Organizers').exists()