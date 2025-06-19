from django import template

register = template.Library()

@register.filter
def is_employee(user):
    return hasattr(user, 'employeeprofile') and user.employeeprofile.is_employee
