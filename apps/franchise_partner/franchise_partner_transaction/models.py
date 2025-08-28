from django.db import models
import uuid
from apps.service_provider.master.models import BaseModel
from apps.franchise_partner.franchise_partner_master.models import Driver, Vehicle


class Device_datatable(BaseModel):
    device_record_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    imei_no = models.CharField(max_length=50, null=True, blank=True) 
    gps_longitude = models.FloatField(null=True, blank=True)  
    gps_latitude = models.FloatField(null=True, blank=True)   
    gps_altitude = models.FloatField(null=True, blank=True)      
    gps_angle = models.FloatField(null=True, blank=True)         
    gps_satellites = models.FloatField(null=True, blank=True)   
    gps_kmh = models.FloatField(null=True, blank=True)
    timestring = models.CharField(max_length=50, null=True, blank=True)

    def str(self):
        return f"Record at longitude {self.gps_longitude} and latitude {self.gps_latitude}"

    
class DeviceSensorDataRecord(models.Model):
    id = models.AutoField(primary_key=True)
    imei_no = models.CharField(max_length=20, null=True, blank=True)
    data_type_code = models.IntegerField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    timestring = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.record_id} - {self.value}"

    
class ReportTable(BaseModel):
    id = models.AutoField(primary_key=True)
    driver = models.CharField(max_length=50, null=True, blank=True)
    license_plate = models.CharField(max_length=255, null=True, blank=True)
    vehicle_id = models.CharField(max_length=50, null=True, blank=True)
    sensor_values = models.JSONField(null=True, blank=True) 
    device_id = models.CharField(max_length=50,null=True, blank=True)
    imei_no = models.CharField(max_length=50, null=True, blank=True)
    batch = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
    

class Maintenance(BaseModel):
    MAINTENANCE_TYPES = [
        ('Fuel', 'Fuel Maintenance'),
        ('Tyre ', 'Tyre  Maintenance'),
        ('Oil', 'Oil Maintenance'),
        ('Maintenance', 'Maintenance'),
    ]

    maintenance_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_related_vehicle',
        null=True,
        blank=True)
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES, default='Fuel')
    quantity = models.CharField(max_length=100, null=True, blank=True)
    kilometer = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.IntegerField(null=True, blank=True)
    tax = models.IntegerField(null=True, blank=True) 
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.maintenance_id}" 


class ReportExportCustomization(BaseModel):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    report_name = models.CharField(max_length=255)  
    columns = models.JSONField()
    filters = models.JSONField(null=True, blank=True)
    sort_order = models.JSONField(null=True, blank=True)  
    isRequired = models.BooleanField(default=False)
    isAutoEmail = models.BooleanField(default=False)
    export_duration = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"Export preferences for {self.report_name} by {self.created_by}"
    
    
class ServiceScheduler(BaseModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='service_assigned_vehicles', null=True, blank=True)
    task = models.TextField(blank=True, null=True)
    service_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    kilometer_last = models.CharField(max_length=255, blank=True, default='', null=False)
    kilometer_reminder = models.CharField(max_length=255, blank=True, default='', null=False)
    notification_type = models.JSONField(default=list) 
    time_reminder = models.IntegerField(blank=True, default='', null=False)
    time_service = models.DateField(blank=True, default='', null=False) 

    def __str__(self):
        return f"{self.title}" 

    
class Geofences(BaseModel):
    CIRCLE = 'circle'
    POLYGON = 'polygon'
    
    GEO_SHAPE_CHOICES = [
        (CIRCLE, 'Circle'),
        (POLYGON, 'Polygon'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    shape = models.CharField(max_length=50, choices=GEO_SHAPE_CHOICES)
    coordinates = models.JSONField()
    vehicle_id = models.ManyToManyField(Vehicle, related_name='geofence_assigned_vehicles', blank=True)

    def __str__(self):
        return f"{self.name}"    
    

class Trip(BaseModel):
    trip_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    trip_name = models.CharField(max_length=255, blank=True)
    start_location_latitude = models.FloatField()
    start_location_longitude = models.FloatField()
    start_location_address = models.TextField()
    end_location_latitude = models.FloatField()
    end_location_longitude = models.FloatField()
    end_location_address = models.TextField()
    waypoints = models.JSONField()
    distance = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    trip_status = models.CharField(max_length=50, choices=[
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ])
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    estimated_start_time = models.DateTimeField()
    estimated_end_time = models.DateTimeField()
    geofence_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.trip_name or "Unnamed Trip"
