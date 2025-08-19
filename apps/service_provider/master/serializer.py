from rest_framework import serializers # type: ignore
from .models import *


def validate_name(value, min_length=3, max_length=255):
    if not (min_length <= len(value) <= max_length):
        raise serializers.ValidationError(f"Name must be between {min_length} and {max_length} characters.")
    if not value.replace(" ", "").isalnum():
        raise serializers.ValidationError("Name must be alphanumeric and contain no special characters.")
    return value

def validate_description(value, min_length=10, max_length=500):
    if not (min_length <= len(value) <= max_length):
        raise serializers.ValidationError(f"Description must be between {min_length} and {max_length} characters.")
    return value


class ValidationMixin:
    def validate_name(self, value):
        return validate_name(value)

    def validate_description(self, value):
        return validate_description(value)


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = '__all__'


class DeviceBrandSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']


class TicketSubCategorySerializer(ValidationMixin, serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = TicketSubCategory
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class TicketCategorySerializer(ValidationMixin, serializers.ModelSerializer):
    subcategories = TicketSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = TicketCategory
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class DeviceTypeSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class VehicleTypeSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class DeviceSensorSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = DeviceSensor
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class VehiclePlateTypeSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = VehiclePlateType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
class DeviceFeatureSerializer(ValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = DeviceFeature
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class DeviceSerializer(ValidationMixin, serializers.ModelSerializer):
    features = serializers.PrimaryKeyRelatedField(
        queryset=DeviceFeature.objects.all(),
        many=True,
        required=False
    )
    sensors = serializers.PrimaryKeyRelatedField(
        queryset=DeviceSensor.objects.all(),
        many=True,
        required=False
    )
    feature_details = serializers.SerializerMethodField()
    sensor_details =  serializers.SerializerMethodField()
    device_type_name = serializers.CharField(source='device_type.device_type_name', read_only=True)
    device_brand_name = serializers.CharField(source='device_brand.device_brand_name', read_only=True)
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_feature_details(self, obj):
        return [feature.feature_name for feature in obj.features.all()]
    def get_sensor_details(self, obj):
        return [sensor.device_sensor_name for sensor in obj.sensors.all()]
class UnitSerializer(ValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
class DeviceDataTypeSerializer(ValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = DeviceDataType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']