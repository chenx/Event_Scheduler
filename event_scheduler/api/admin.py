from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Event, EventUser, Notification, NotificationUser, NotificationStatus, CustomUser


admin.site.register(Event)
admin.site.register(EventUser)
admin.site.register(Notification)
admin.site.register(NotificationUser)
admin.site.register(NotificationStatus)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = UserAdmin.add_fieldsets + (
        (('Custom Fields', {'fields': ('phone',)}),)
    )
    fieldsets = UserAdmin.fieldsets + (
        (('Custom Fields', {'fields': ('phone', )}),)
    )

admin.site.register(CustomUser, CustomUserAdmin)