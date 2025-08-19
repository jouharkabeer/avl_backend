from django.contrib import admin

from .models import *

class DeviceDatatableAdmin(admin.ModelAdmin):
    list_display = ('device_record_id', 'imei_no', 'gps_longitude', 'gps_latitude', 'created_at')
    search_fields = ('imei_no',)
    list_filter = ('created_at',)

class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['maintenance_id', 'vehicle', 'maintenance_type', 'total_amount']
    search_fields = ['maintenance_id', 'vehicle__id']
    
class ServiceSchedulerAdmin(admin.ModelAdmin):
    
    list_display = (
        'id', 
        'title', 
        'vehicle_id', 
        'service_date', 
        'email', 
        'kilometer_last', 
        'kilometer_reminder', 
        'time_reminder', 
        'time_service',
    )

    
    search_fields = ('title', 'email', 'vehicle_id__id')  

   
    list_filter = ('service_date', 'notification_type', 'vehicle_id')

    
    fields = (
        'title', 
        'vehicle_id', 
        'task', 
        'service_date', 
        'email', 
        'kilometer_last', 
        'kilometer_reminder', 
        'notification_type', 
        'time_reminder', 
        'time_service',
    )

    # Read-only fields if required
    readonly_fields = ('id',)
    
    
class GeofencesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shape')  # Display ID, name, and shape in the list view
    search_fields = ('name',)  # Enable search by name
    list_filter = ('shape',)  # Filter by shape type
    filter_horizontal = ('vehicle_id',) 

admin.site.register(Device_datatable, DeviceDatatableAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(ServiceScheduler, ServiceSchedulerAdmin)
admin.site.register(Geofences, GeofencesAdmin)