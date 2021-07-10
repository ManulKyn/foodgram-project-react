from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from backend.users.models import User

class PersonAdmin(UserAdmin):
    list_filter = ('email', 'username',)


admin.site.unregister(User)
admin.site.register(User, PersonAdmin)
