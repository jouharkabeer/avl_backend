from rest_framework import serializers
from apps.service_provider.master.serializer import DeviceSerializer
from .models import *
from apps.service_provider.master.serializer import ValidationMixin
import logging

logger = logging.getLogger(__name__)
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'file', 'document_type']

class DriverSerializer(serializers.ModelSerializer):
    # documents = DocumentSerializer(many=True)
    class Meta:
        model = Driver
        fields = [
            'first_name', 'last_name', 'license_number', 
            'date_of_birth', 'address', 'phone_number', 
            'email', 'documents','account','driver_id',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('context', {}).get('request', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        account_id = self.request.data.get('account_id')
        if account_id:
            account = Account.objects.get(pk=account_id)
            validated_data['account'] = account
        documents_data = validated_data.pop('documents', [])
        driver = Driver.objects.create(**validated_data)
        documents_data = []
        index = 0
        
        # Loop through potential document indices
        while True:
            name_key = f'documents[{index}][name]'
            type_key = f'documents[{index}][document_type]'
            file_key = f'documents[{index}][file]'

            # Check if the document name exists; if not, break the loop
            if name_key not in self.request.data:
                break

            # Collect the document data
            document = {
                'name': self.request.data.getlist(name_key)[0],
                'document_type': self.request.data.getlist(type_key)[0],
                'file': self.request.data.getlist(file_key)[0],  # Handle file upload
            }
            documents_data.append(document)
            index += 1

        # Create Document instances from the collected data
        for doc_data in documents_data:
            doc_type, created = DocumentType.objects.get_or_create(name=doc_data['document_type'])
            Document.objects.create(
                driver=driver,
                name=doc_data['name'],
                file=doc_data['file'],  # Ensure file is handled correctly
                document_type=doc_type
            )
        return driver

    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents', [])
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.license_number = validated_data.get('license_number', instance.license_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        # Update or create documents
        for document_data in documents_data:
            document_id = document_data.get('document_id')
            if document_id:
                # Update existing document
                document = Document.objects.get(id=document_id, driver=instance)
                document.name = document_data.get('name', document.name)
                document.file = document_data.get('file', document.file)
                document.document_type = document_data.get('document_type', document.document_type)
                document.save()
            else:
                # Create new document
                Document.objects.create(driver=instance, **document_data)
        
        return instance


class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'file', 'document_type']


class VehicleSerializer(serializers.ModelSerializer):
    # documents = VehicleDocumentSerializer(many=True)
   
    class Meta:
        model = Vehicle
        fields = ['make', 'model','body_type', 'year', 'license_plate', 'vin', 'color', 'account', 'driver', 'documents','vehicle_id','maintenance_period']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('context', {}).get('request', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        account_id = self.request.data.get('account_id')
        if account_id:
            account = Account.objects.get(pk=account_id)
            validated_data['account'] = account
        documents_data = validated_data.pop('documents', [])
        vehicle = Vehicle.objects.create(**validated_data)
        documents_data = []
        index = 0
        
        # Loop through potential document indices
        while True:
            name_key = f'documents[{index}][name]'
            type_key = f'documents[{index}][document_type]'
            file_key = f'documents[{index}][file]'

            # Check if the document name exists; if not, break the loop
            if name_key not in self.request.data:
                break

            # Collect the document data
            document = {
                'name': self.request.data.getlist(name_key)[0],
                'document_type': self.request.data.getlist(type_key)[0],
                'file': self.request.data.getlist(file_key)[0],  # Handle file upload
            }
            documents_data.append(document)
            index += 1

        # Create Document instances from the collected data
        for doc_data in documents_data:
            doc_type, created = DocumentType.objects.get_or_create(name=doc_data['document_type'])
            Document.objects.create(
                vehicle=vehicle,
                name=doc_data['name'],
                file=doc_data['file'],  # Ensure file is handled correctly
                document_type=doc_type
            )
        return vehicle


    def update(self, instance, validated_data):
        logger.info('Creating a vehicle and its documents...')
        documents_data = validated_data.pop('documents', [])
        
        # Update vehicle fields
        instance.make = validated_data.get('make', instance.make)
        instance.model = validated_data.get('model', instance.model)
        instance.maintenance_period = validated_data.get('maintenance_period', instance.maintenance_period)
        instance.year = validated_data.get('year', instance.year)
        instance.license_plate = validated_data.get('license_plate', instance.license_plate)
        instance.vin = validated_data.get('vin', instance.vin)
        instance.color = validated_data.get('color', instance.color)
        instance.driver = validated_data.get('driver', instance.driver)
        instance.body_type = validated_data.get('body_type', instance.body_type)
        instance.save()

        # Handle document updates
        existing_docs = {doc.document_id: doc for doc in instance.documents.all()}
        for document_data in documents_data:
            document_id = document_data.get('document_id')
            if document_id and document_id in existing_docs:
                # Update existing document
                document = existing_docs[document_id]
                document.name = document_data.get('name', document.name)
                document.file = document_data.get('file', document.file)
                document.document_type = document_data.get('document_type', document.document_type)
                document.save()
            else:
                # Create new document
                Document.objects.create(vehicle=instance, **document_data)
        
        return instance


class DocumentTypeSerializer(ValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
class  AccountTypeSerializer(ValidationMixin, serializers.ModelSerializer):
    class Meta:
        model =  AccountType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
class AccountSerializer(serializers.ModelSerializer):
    account_type_name = serializers.CharField(source='account_type.account_type_name', read_only=True)
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class AccountDeviceSerializer(serializers.ModelSerializer):
    features = serializers.PrimaryKeyRelatedField(
        queryset=DeviceFeature.objects.all(),
        many=True,
        required=False
    )
    feature_details = serializers.SerializerMethodField()
    vehicle_id = serializers.UUIDField(source='vehicle.vehicle_id', read_only=True)
    license_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)

    class Meta:
        model = AccountDevice
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_feature_details(self, obj):
        return [feature.feature_name for feature in obj.features.all()]


class VehicleListSerializer(ValidationMixin,serializers.ModelSerializer):
    body_type_name = serializers.CharField(source='body_type.vehicle_type_name', read_only=True)
    deriver_name =serializers.CharField(source="driver.get_full_name", read_only=True)
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class DriverListSerializer(ValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class OrderListSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.name', read_only=True)
    device_name = serializers.CharField(source='device.device_name', read_only=True)
    features_list = serializers.SerializerMethodField()
    sensors_list = serializers.SerializerMethodField()  # New field for sensors

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_features_list(self, obj):
        return [
            {
                'id': feature.feature_id,
                'feature_name': feature.feature_name
            } for feature in obj.features.all()
        ]
    
    def get_sensors_list(self, obj):
        return [
            {
                'id': sensor.device_sensor_id,
                'sensor_name': sensor.device_sensor_name
            } for sensor in obj.sensors.all()  
        ]

class DeviceOrderSerializer(serializers.Serializer):
    device_id = serializers.UUIDField(source='device__device_id')
    device_name = serializers.CharField(source='device__device_name')
    total_quantity = serializers.IntegerField()
        
class DevicefeatureSerializer(ValidationMixin, serializers.ModelSerializer):
    feature_details = serializers.SerializerMethodField()
    class Meta:
        model = Device
        fields = ['feature_details']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_feature_details(self, obj):
        features = obj.features.all().order_by('-is_default') 
        return [{'id': feature.feature_id, 'name': feature.feature_name, 'default': feature.is_default} for feature in features]    

class SubscriptionSerializer(serializers.ModelSerializer):
    acount_name = serializers.CharField(source="account.name",read_only=True)
    device_name = serializers.CharField(source="device.device_name",read_only=True)
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

