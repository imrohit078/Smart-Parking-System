from django.contrib import admin
from .models import PlateSession, EmployeeProfile, Employee
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
@admin.register(PlateSession)
class PlateSessionAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'vehicle_type', 'entry_time', 'exit_time', 'display_charge', 'is_paid')
    list_filter = ('vehicle_type', 'is_paid')
    search_fields = ('plate_number',)

    fields = ('plate_number', 'vehicle_type', 'entry_time', 'exit_time', 'is_paid')
    readonly_fields = ('entry_time',)

    actions = ['mark_as_paid']

    def display_charge(self, obj):
        return f"₹ {obj.charge}" if obj.charge else "Pending"
    display_charge.short_description = 'Charge (INR)'

    @admin.action(description='✅ Mark selected sessions as Paid')
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(is_paid=True)
        self.message_user(request, f"{updated} session(s) marked as paid.")


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'role', 'is_employee')
    list_filter = ('is_employee', 'role')
    search_fields = ('user__username',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'role')
    search_fields = ('user__username', 'user__email', 'phone')