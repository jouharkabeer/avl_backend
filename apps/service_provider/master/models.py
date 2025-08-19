import uuid
from django.db import models  # type: ignore
from django.core.validators import RegexValidator  # type: ignore
from apps.authentication.models import User


class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
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


class ChangeLog(models.Model):
    ACTION_CHOICES = [
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    ]
    
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_name = models.CharField(max_length=100) 
    object_id = models.UUIDField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    is_delete = models.BooleanField(default=False)  
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField()
    
    def __str__(self):
        return f"{self.model_name} edited by {self.edited_by} on {self.edited_at}"


class DeviceBrand(BaseModel):
    device_brand_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_brand_name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Device brand name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    
    def __str__(self):
        return self.device_brand_name


class TicketCategory(BaseModel):
    ticket_category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Ticket category name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    
    def __str__(self):
        return self.name


class TicketSubCategory(BaseModel):
    ticket_subcategory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Ticket Subcategory name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    category = models.ForeignKey(
        TicketCategory,
        related_name='subcategories',
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f"{self.name} (Category: {self.category.name})"


class DeviceType(BaseModel):
    device_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_type_name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Device Type name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    
    def __str__(self):
        return self.device_type_name


class VehicleType(BaseModel):
    vehicle_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_type_name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Vehicle type name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    
    def __str__(self):
        return self.vehicle_type_name


class DeviceSensor(BaseModel):
    device_sensor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_sensor_name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Device sensor name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    
    def __str__(self):
        return self.device_sensor_name


class VehiclePlateType(BaseModel):
    vehicle_plate_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Vehicle plate type name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    
    def __str__(self):
        return self.name


class DeviceFeature(BaseModel):
    feature_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feature_name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Feature name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    is_default = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.feature_name


class Device(BaseModel):
    device_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Device name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    device_brand = models.ForeignKey(DeviceBrand, on_delete=models.CASCADE)
    sensors = models.ManyToManyField(DeviceSensor, related_name='devices')
    features = models.ManyToManyField(DeviceFeature, related_name='devices')

    def __str__(self):
        return self.device_name


class Unit(BaseModel):
    unit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit_name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message='Unit name must be alphanumeric and contain no special characters.'
            )
        ]
    )
    description = models.TextField()
    symbol = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        ordering = ['unit_name']
        indexes = [
            models.Index(fields=['unit_name']),
        ]
        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        return f"{self.unit_name} ({self.symbol})"

    
class DeviceDataType(BaseModel):
    device_dataType_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_type_code = models.CharField(max_length=50)
    data_type_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    device_value_meaning = models.JSONField()  
    supported_devices = models.JSONField()
    showdatatype = models.BooleanField(default=True)
    iscalculateddatatype = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.data_type_name} - {self.device_value_meaning}"
