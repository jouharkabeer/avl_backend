from django.db import models
import uuid
from apps.service_provider.master.models import BaseModel,DeviceFeature, DeviceSensor,User,VehicleType
from django.core.validators import RegexValidator
from apps.service_provider.master.models import Device

class AccountType(BaseModel):
    account_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_type_name = models.CharField(
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
        return self.account_type_name
class Account(BaseModel):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    parent_account = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='client_accounts')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_accounts')
    def __str__(self):
        return self.name

class DocumentType(BaseModel):
    documentype_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    def __str__(self):
        return self.name


class Document(BaseModel):
    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    document_type = models.ForeignKey(DocumentType, related_name='documnettype', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: You could leave out direct relations here for simplicity
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, related_name='document_related_driver', null=True, blank=True)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='document_related_vehicle', null=True, blank=True)
    
    def __str__(self):
        associations = []
        if self.driver:
            associations.append(f"Driver: {self.driver}")
        if self.vehicle:
            associations.append(f"Vehicle: {self.vehicle}")
        return f"{self.name} ({', '.join(associations)})"

class Driver(BaseModel):
    driver_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    # Many-to-many relationship with Document
    documents = models.ManyToManyField(Document, related_name='drivers', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Vehicle(BaseModel):
    vehicle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='vehicles',null=True, blank=True)
    body_type = models.ForeignKey(VehicleType,on_delete=models.CASCADE, related_name='Vehicle_type',null=True,blank=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=30)
    maintenance_period =models.CharField(max_length=50,null=True)

    # Many-to-many relationship with Document
    documents = models.ManyToManyField(Document, related_name='vehicles', blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class AccountDevice(BaseModel):
    account_device_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='Account_devices')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='Account_assigned_devices')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='Account_assigned_vehicles', null=True, blank=True)
    serial_no = models.CharField(max_length=50, null=True, blank=True)
    imei_no = models.CharField(max_length=50, null=True, blank=True)
    features = models.ManyToManyField(DeviceFeature, related_name='devices_features')
    configuration_api = models.CharField(max_length=50, null=True, blank=True)
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE, null=True, related_name='Account_subscription')
    def __str__(self):
        return f"{self.account.name} - {self.device.device_name}"
    
class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='orders')
    features = models.ManyToManyField(DeviceFeature, related_name='ordered_features', blank=True)
    sensors = models.ManyToManyField(DeviceSensor, related_name='orders', blank=True)  # New field for sensors
    quantity = models.PositiveIntegerField(default=1)
    cancel_reason =models.CharField(max_length=50, null=True, blank=True)
    order_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order {self.order_id} by {self.account.name} for {self.device.device_name} ({self.quantity} units)"

class Subscription(BaseModel):
    subscription_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='Subscription_account')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='subscription_assigned_devices')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_against_subscription')
    subscription_name = models.CharField(max_length=30, null=False)
    count = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.subscription_name}"
