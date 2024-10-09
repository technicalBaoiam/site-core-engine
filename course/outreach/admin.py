from django.contrib import admin
from .models import Contact, StudentEnrollment


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')
   

# Register your admin class
admin.site.register(Contact, ContactAdmin)
admin.site.register(StudentEnrollment)
