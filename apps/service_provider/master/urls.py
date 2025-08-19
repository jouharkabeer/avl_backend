# type: ignore
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # DeviceBrand URLs
    path('device-brand/', DeviceBrandListView.as_view(), name='device-brand-list'),
    path('device-brand/create/', DeviceBrandCreateView.as_view(), name='device-brand-create'),
    path('device-brand/update/<uuid:pk>/', DeviceBrandUpdateView.as_view(), name='device-brand-update'),
    path('device-brand/delete/<uuid:pk>/', DeviceBrandDeleteView.as_view(), name='device-brand-delete'),

    # TicketCategory URLs
    path('ticket-category/', TicketCategoryListView.as_view(), name='ticket-category-list'),
    path('ticket-category/create/', TicketCategoryCreateView.as_view(), name='ticket-category-create'),
    path('ticket-category/update/<uuid:pk>/', TicketCategoryUpdateView.as_view(), name='ticket-category-update'),
    path('ticket-category/delete/<uuid:pk>/', TicketCategoryDeleteView.as_view(), name='ticket-category-delete'),

    # TicketSubCategory URLs
    path('ticket-sub-category/', TicketSubCategoryListView.as_view(), name='ticket-sub-category-list'),
    path('ticket-sub-category/create/', TicketSubCategoryCreateView.as_view(), name='ticket-sub-category-create'),
    path('ticket-sub-category/update/<uuid:pk>/', TicketSubCategoryUpdateView.as_view(), name='ticket-sub-category-update'),
    path('ticket-sub-category/delete/<uuid:pk>/', TicketSubCategoryDeleteView.as_view(), name='ticket-sub-category-delete'),

    # DeviceType URLs
    path('device-type/', DeviceTypeListView.as_view(), name='device-type-list'),
    path('device-type/create/', DeviceTypeCreateView.as_view(), name='device-type-create'),
    path('device-type/update/<uuid:pk>/', DeviceTypeUpdateView.as_view(), name='device-type-update'),
    path('device-type/delete/<uuid:pk>/', DeviceTypeDeleteView.as_view(), name='device-type-delete'),

    # VehicleType URLs
    path('vehicle-type/', VehicleTypeListView.as_view(), name='vehicle-type-list'),
    path('vehicle-type/create/', VehicleTypeCreateView.as_view(), name='vehicle-type-create'),
    path('vehicle-type/update/<uuid:pk>/', VehicleTypeUpdateView.as_view(), name='vehicle-type-update'),
    path('vehicle-type/delete/<uuid:pk>/', VehicleTypeDeleteView.as_view(), name='vehicle-type-delete'),

    # DeviceSensor URLs
    path('device-sensor/', DeviceSensorListView.as_view(), name='device-sensor-list'),
    path('device-sensor/create/', DeviceSensorCreateView.as_view(), name='device-sensor-create'),
    path('device-sensor/update/<uuid:pk>/', DeviceSensorUpdateView.as_view(), name='device-sensor-update'),
    path('device-sensor/delete/<uuid:pk>/', DeviceSensorDeleteView.as_view(), name='device-sensor-delete'),

    # VehiclePlateType URLs
    path('vehicle-plate-type/', VehiclePlateTypeListView.as_view(), name='vehicle-plate-type-list'),
    path('vehicle-plate-type/create/', VehiclePlateTypeCreateView.as_view(), name='vehicle-plate-type-create'),
    path('vehicle-plate-type/update/<uuid:pk>/', VehiclePlateTypeUpdateView.as_view(), name='vehicle-plate-type-update'),
    path('vehicle-plate-type/delete/<uuid:pk>/', VehiclePlateTypeDeleteView.as_view(), name='vehicle-plate-type-delete'),

      # DeviceFeature URLs
    path('device-features/', DeviceFeatureListView.as_view(), name='device-feature-list'),
    path('device-features/create/', DeviceFeatureCreateView.as_view(), name='device-feature-create'),
    path('device-features/<uuid:pk>/update/', DeviceFeatureUpdateView.as_view(), name='device-feature-update'),
    path('device-features/<uuid:pk>/delete/', DeviceFeatureDeleteView.as_view(), name='device-feature-delete'),

    # Device URLs
    path('devices/', DeviceListView.as_view(), name='device-list'),
    path('devices/create/', DeviceCreateView.as_view(), name='device-create'),
    path('devices/<uuid:pk>/update/', DeviceUpdateView.as_view(), name='device-update'),
    path('devices/<uuid:pk>/delete/', DeviceDeleteView.as_view(), name='device-delete'),

    # Unit URLs
    path('units/', UnitListView.as_view(), name='unit-list'),
    path('units/create/', UnitCreateView.as_view(), name='unit-create'),
    path('units/<uuid:pk>/update/', UnitUpdateView.as_view(), name='unit-update'),
    path('units/<uuid:pk>/delete/', UnitDeleteView.as_view(), name='unit-delete'),

    
    # DeviceDataType URLs
    path('DeviceDataType/', DeviceDataTypeListView.as_view(), name='DeviceDataType-list'),
    path('DeviceDataType/create/', DeviceDataTypeCreateView.as_view(), name='DeviceDataType-create'),
    path('DeviceDataType/<uuid:pk>/update/', DeviceDataTypeUpdateView.as_view(), name='DeviceDataType-update'),

]