
from rest_framework import serializers
from .models import *
from ..franchise_partner_master.models import AccountDevice
from  apps.service_provider.master.models import  DeviceDataType


class DeviceDatatableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device_datatable
        fields = ['device_record_id', 'gps_longitude', 'gps_latitude', 'gps_altitude', 'gps_angle', 
                  'gps_satellites', 'gps_kmh', 'created_at','timestring']
        
class DeviceDatatableGroupedSerializer(serializers.Serializer):
    imei_no = serializers.CharField()
    vehicle_id =serializers.UUIDField()
    vehicle_regno = serializers.CharField()
    record_count = serializers.IntegerField()
    records = DeviceDatatableSerializer(many=True)


class DeviceValueSerializer(serializers.Serializer):
    data_type_code = serializers.IntegerField()
    data_type_name = serializers.CharField()
    value = serializers.IntegerField()
    timestring = serializers.CharField()
    meaning = serializers.CharField(required=False, allow_null=True)

class VehicleDataSerializer(serializers.Serializer):
    vehicle_id = serializers.UUIDField()
    license_plate = serializers.CharField()
    device_values = DeviceValueSerializer(many=True)

class CombinedVehicleDataSerializer(serializers.Serializer):
    imei_no = serializers.CharField()
    vehicle_id = serializers.IntegerField(allow_null=True)
    license_plate = serializers.CharField(allow_null=True)
    record_count = serializers.IntegerField()
    records = serializers.ListField()
    device_values = serializers.ListField()

class  ReportTableSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ReportTable
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)
    class Meta:
        model = Maintenance
        fields = '__all__'
        read_only_fields = ['maintenance_id', 'amount', 'tax', 'created_at', 'updated_at']

    TAX_RATE = 0.15  # Define tax rate as a class constant

    def validate(self, data):
        
        if int(data.get('quantity', 0)) <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be greater than zero."})
        
        
        kilometer = data.get('kilometer', None)
        if kilometer is not None:
            if not isinstance(kilometer, int):
                raise serializers.ValidationError({"kilometer": "Kilometer must be an integer."})
            if kilometer < 0:
                raise serializers.ValidationError({"kilometer": "Kilometer must be greater than or equal to zero."})
        
      
        total_amount = data.get('total_amount', None)
        if total_amount is None or total_amount <= 0:
            raise serializers.ValidationError({"total_amount": "Total amount must be greater than zero."})
        
        return data

    def create(self, validated_data):
        
        total_amount = validated_data.get('total_amount', 0)
        validated_data['tax'] = total_amount * self.TAX_RATE
        validated_data['amount'] = total_amount - validated_data['tax']
        
       
        return super().create(validated_data)
    
    
class CustomDeviceDataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDataType
        fields = ['data_type_name', 'data_type_code']

class ReportExportCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExportCustomization
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class ReportExportCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExportCustomization
        fields = ['id', 'report_name']
        
        
class ServiceShedulerSerializer(serializers.ModelSerializer):
    # vehicle_id = serializers.UUIDField(source='vehicle.vehicle_id', read_only=True)
    license_plate = serializers.CharField(source='vehicle_id.license_plate', read_only=True)
    maintenance_period = serializers.CharField(source='vehicle_id.maintenance_period', read_only=True)

    class Meta:
        model = ServiceScheduler
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']        
    def validate(self, attrs):
        # Extract the relevant fields from the validated data
        time_service = attrs.get('time_service')
        time_reminder = attrs.get('time_reminder')
        kilometer_last = attrs.get('kilometer_last')
        kilometer_reminder = attrs.get('kilometer_reminder')

        # Validation logic
        if (time_service or time_reminder) and (kilometer_last or kilometer_reminder):
            # If both time and kilometer fields are provided, allow it
            return attrs

        if not (time_service or time_reminder) and not (kilometer_last or kilometer_reminder):
            raise serializers.ValidationError(
                "Either time_service and time_reminder, or kilometer_last and kilometer_reminder must be provided."
            )

        return attrs
    
    
class GeofenceSerializer(serializers.ModelSerializer):
    license_plate = serializers.SerializerMethodField()
   

    class Meta:
        model = Geofences
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']     
        
    def get_license_plate(self, obj):
        # Get the license plates of the associated vehicles as a list
        vehicle_licenses = obj.vehicle_id.values_list('license_plate', flat=True)
        return list(vehicle_licenses)     
    

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ['trip_id']