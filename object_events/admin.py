"""Admin classes for the ``object_events`` app."""
from django.contrib import admin

from .models import ObjectEvent, ObjectEventType


class ObjectEventTypeAdmin(admin.ModelAdmin):
    list_display = ['title', ]


class ObjectEventAdmin(admin.ModelAdmin):
    list_display = [
        'user_email', 'content_object', 'type_title', 'creation_date', ]

    def content_object(self, obj):
        return obj.content_object
    content_object.short_description = 'Content object'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'

    def type_title(self, obj):
        return obj.event_type.title
    type_title.short_description = 'Type'


admin.site.register(ObjectEvent, ObjectEventAdmin)
admin.site.register(ObjectEventType, ObjectEventTypeAdmin)
