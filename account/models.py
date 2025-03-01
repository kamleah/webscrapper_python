from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class RoleModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} | {self.name}"


class CustomUser(AbstractUser):
    user_role = models.ForeignKey(
        RoleModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    user_created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users",
    )
    process_type = models.TextField(default="single", null=False, blank=False)

    # Avoid conflicts with AbstractUser
    groups = models.ManyToManyField(Group, related_name="custom_groups", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_permissions", blank=True
    )

    def __str__(self):
        return self.username


class UserRoleModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    role = models.ForeignKey(
        RoleModel, on_delete=models.CASCADE, blank=True, null=True, default=None
    )

    def __str__(self):
        return f"{self.id} | {self.user.username} | {self.role.name}"
