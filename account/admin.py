from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Member

admin.site.register(Member, UserAdmin)
