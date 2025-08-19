import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        self.is_delete = True
        self.save()

    def restore(self):
        self.is_delete = False
        self.save()


class Permission(BaseModel):
    permission_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission_name = models.CharField(max_length=125)
    is_view = models.BooleanField(default=False)
    is_add = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    is_details = models.BooleanField(default=False)

    class Meta:
        ordering = ('permission_name',)
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")

    def __str__(self):
        return self.permission_name


class Role(BaseModel):
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=125)
    permissions = models.ManyToManyField(Permission, related_name='roles', blank=True)

    class Meta:
        ordering = ('role_name',)
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.role_name

    def delete(self, *args, **kwargs):
        self.permissions.update(is_delete=True)
        super().delete(*args, **kwargs)


class UserType(BaseModel):
    user_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type_name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('user_type_name',)
        verbose_name = _("User Type")
        verbose_name_plural = _("User Types")

    def __str__(self):
        return self.user_type_name


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_role = models.ForeignKey(Role, on_delete=models.RESTRICT, null=True, blank=True)
    individual_permissions = models.ManyToManyField(Permission, related_name='users', blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    user_type = models.ForeignKey(UserType, on_delete=models.RESTRICT, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='profile_images/default.png')
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    account = models.ForeignKey('franchise_partner_master.Account', on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if self.pk is None or not self._state.adding and 'password' in self.__dict__:
            if self.password and not self.password.startswith('pbkdf2_'):
                self.set_password(self.password)
        super().save(*args, **kwargs)

    def has_permission(self, permission_type):
        role_permissions = self.user_role.permissions.all() if self.user_role else []
        for perm in role_permissions:
            if getattr(perm, permission_type, False):
                return True
        return self.individual_permissions.filter(**{permission_type: True}).exists()
