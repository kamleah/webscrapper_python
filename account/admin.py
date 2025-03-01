from django.contrib import admin
from .models import RoleModel, UserRoleModel

admin.site.register(RoleModel)
admin.site.register(UserRoleModel)
