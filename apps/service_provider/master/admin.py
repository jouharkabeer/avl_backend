from django.contrib import admin
from .models import (
    DeviceBrand,
    TicketCategory,
    TicketSubCategory,
    DeviceType,
    VehicleType,
    DeviceSensor,
    VehiclePlateType,
    DeviceFeature,
    Device,
    Unit,
    ChangeLog,
)

@admin.register(DeviceBrand)
class DeviceBrandAdmin(admin.ModelAdmin):
    list_display = ('device_brand_name', 'description', 'status', 'is_delete')
    search_fields = ('device_brand_name',)

@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'is_delete')
    search_fields = ('name',)

@admin.register(TicketSubCategory)
class TicketSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'is_delete')
    search_fields = ('name',)
    
@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('device_type_name', 'description', 'status', 'is_delete')
    search_fields = ('device_type_name',)

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type_name', 'description', 'status', 'is_delete')
    search_fields = ('vehicle_type_name',)

@admin.register(DeviceSensor)
class DeviceSensorAdmin(admin.ModelAdmin):
    list_display = ('device_sensor_name', 'description', 'status', 'is_delete')
    search_fields = ('device_sensor_name',)

@admin.register(VehiclePlateType)
class VehiclePlateTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'is_delete')
    search_fields = ('name',)

@admin.register(DeviceFeature)
class DeviceFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name', 'description', 'is_default', 'status', 'is_delete')
    search_fields = ('feature_name',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_type', 'device_brand', 'status', 'is_delete')
    search_fields = ('device_name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_name', 'symbol', 'status', 'is_delete')
    search_fields = ('unit_name',)

@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'object_id', 'action', 'edited_by', 'edited_at')
    search_fields = ('model_name', 'action')
