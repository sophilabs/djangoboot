from django.contrib import admin
from accounts.models import User, Team

admin.site.register(User)
admin.site.register(Team)