from django.http import HttpResponseForbidden

def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'employeeprofile') and request.user.employeeprofile.is_employee:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("🚫 Access Denied: Employees Only")
    return wrapper
