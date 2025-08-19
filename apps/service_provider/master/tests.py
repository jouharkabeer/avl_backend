from django.test import TestCase

# Create your tests here.
from django.core.exceptions import ValidationError
from django.test import TestCase
from apps.authentication.models import User,Permission
from .models import VehicleType
from .serializer import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class VehicleTypeModelTests(TestCase):
    def setUp(self):

        self.vehicle_type = VehicleType.objects.create(
            vehicle_type_name='Sedan124',
            description='A small car with a separate trunk.'
        )
    
    def test_vehicle_type_creation(self):

        self.assertEqual(self.vehicle_type.vehicle_type_name, 'Sedan124')
        self.assertEqual(self.vehicle_type.description, 'A small car with a separate trunk.')
        self.assertEqual(self.vehicle_type.status, 'active')
        self.assertTrue(self.vehicle_type.created_at is not None)
        self.assertTrue(self.vehicle_type.updated_at is not None)

    def test_vehicle_type_string_representation(self):
    
        self.assertEqual(str(self.vehicle_type), 'Sedan124')

    def test_default_status(self):

        vehicle_type = VehicleType.objects.create(
            vehicle_type_name='SUV1245',
            description='A larger vehicle designed for off-road driving.'
        )
        self.assertEqual(vehicle_type.status, 'active')


    def test_valid_vehicle_type_name(self):
        # Test valid alphanumeric device type name
        data = {'vehicle_type_name': 'Valid123', 'description': 'A valid device type.', 'status': 'active'}
        serializer =VehicleTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_vehicle_type_name(self):
        # Test invalid device type name containing special characters
        data = {'vehicle_type_name': 'Invalid@Name!', 'description': 'An invalid device type.', 'status': 'active'}
        serializer = VehicleTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['vehicle_type_name'][0], "Device type name must be alphanumeric and have no special characters.")
class DeviceSensorTests(APITestCase):

    def setUp(self):
        self.user_permission = Permission.objects.create(is_view=True, is_add=True, is_edit=True)
        self.user = User.objects.create(username='testuser', user_permission_id=self.user_permission)  # Assign the Permission instance directly
        self.client.force_authenticate(user=self.user)

        self.device_sensor = DeviceSensor.objects.create(device_sensor_name='Temperature', description='Temperature sensor', status=True, created_by=self.user.username)

    def test_list_device_sensors(self):
        url = reverse('devicesensors-list')
        response = self.client.get(url, {'user_id': self.user.user_id})

        self.assertEqual(len(response.data), 1)
        



    def test_create_device_sensor_duplicate_name(self):
        url = reverse('devicesensors-create')
        data = {'device_sensor_name': 'Temperature', 'description': 'Another temperature sensor', 'status': True}
        response = self.client.post(url, data, format='json')

        self.assertIn('device sensor with this device sensor name already exists.', response.data['device_sensor_name'])

    def test_create_device_sensor_invalid_name(self):
        url = reverse('devicesensors-create')
        data = {'device_sensor_name': 'Temp@123', 'description': 'Invalid name sensor', 'status': True}
        response = self.client.post(url, data, format='json')

        self.assertIn('Device sensor name must be alphanumeric and contain no special characters.', response.data['device_sensor_name'])

    def test_create_device_sensor_invalid_description(self):
        url = reverse('devicesensors-create')
        data = {'device_sensor_name': 'Humidity', 'description': '<script>alert("test")</script>', 'status': True}
        response = self.client.post(url, data, format='json')

        self.assertIn('Description must not contain HTML tags or non-English characters.', response.data['description'])

    def test_update_device_sensor(self):
        url = reverse('devicesensors-update', args=[self.device_sensor.device_sensor_id])
        data = {'device_sensor_name': 'Temperature', 'description': 'Updated description', 'status': True}
        response = self.client.put(url, data, format='json')
        self.device_sensor.refresh_from_db()
 

    def test_update_device_sensor_duplicate_name(self):
        another_sensor = DeviceSensor.objects.create(device_sensor_name='Pressure', description='Pressure sensor', status=True, created_by=self.user.username)
        url = reverse('devicesensors-update', args=[another_sensor.device_sensor_id])
        data = {'device_sensor_name': 'Temperature', 'description': 'Duplicate name sensor', 'status': True}
        response = self.client.put(url, data, format='json')
        self.assertIn('device sensor with this device sensor name already exists.', response.data['device_sensor_name'])


    def test_update_device_sensor_invalid_description(self):
        url = reverse('devicesensors-update', args=[self.device_sensor.device_sensor_id])
        data = {'device_sensor_name': 'Temperature', 'description': '<script>alert("test")</script>', 'status': True}
        response = self.client.put(url, data, format='json')
        self.assertIn('Description must not contain HTML tags or non-English characters.', response.data['description'])


class VehiclePlateTypeModelTests(TestCase):
    def setUp(self):
        self.vehicle_plate_type = VehiclePlateType.objects.create(
            name='Commercial',
            description='A plate type for commercial vehicles.',
            created_by='test_user'
        )

    def test_vehicle_plate_type_creation(self):
        self.assertEqual(self.vehicle_plate_type.name, 'Commercial')
        self.assertEqual(self.vehicle_plate_type.description, 'A plate type for commercial vehicles.')
        self.assertEqual(self.vehicle_plate_type.status, True)
        self.assertEqual(self.vehicle_plate_type.is_delete, False)
        self.assertEqual(self.vehicle_plate_type.created_by, 'test_user')
        self.assertTrue(self.vehicle_plate_type.created_at is not None)
        self.assertTrue(self.vehicle_plate_type.updated_at is not None)

    def test_vehicle_plate_type_string_representation(self):
        self.assertEqual(str(self.vehicle_plate_type), 'Commercial')

    def test_default_status(self):
        vehicle_plate_type = VehiclePlateType.objects.create(
            name='Personal',
            description='A plate type for personal vehicles.',
            created_by='test_user2'
        )
        self.assertEqual(vehicle_plate_type.status, True)

    def test_valid_vehicle_plate_type_name(self):
        data = {'name': 'Valid123', 'description': 'A valid plate type.', 'status': True, 'created_by': 'test_user3'}
        serializer = VehiclePlateTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_vehicle_plate_type_name(self):
        data = {'name': 'Invalid@Name!', 'description': 'An invalid plate type.', 'status': True, 'created_by': 'test_user4'}
        serializer = VehiclePlateTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['name'][0], "Vehicle plate type name must be alphanumeric and contain no special characters.")