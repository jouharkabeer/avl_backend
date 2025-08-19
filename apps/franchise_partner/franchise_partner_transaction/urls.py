from django.urls import path
from .views import*

urlpatterns = [
path('latest-vehicle-data/', LatestVehicleDataView.as_view(), name='latest-data'),
path('report-table-data', ReportTableListView.as_view(), name='report-table-data-by-time'),
path('gps-data', GpsDataListView.as_view(), name='gps-data'),


path('maintenancecreate/', MaintenanceCreateView.as_view(), name='maintenance-create'),
path('maintenancelist/', MaintenanceListView.as_view(), name='maintenance-list'),
path('maintenance/<uuid:pk>/update', MaintenanceUpdateView.as_view(), name='maintenance-update'),
path('maintenance/<uuid:pk>/delete/', MaintenanceDeleteView.as_view(), name='maintenance-delete'),



path('custom_device-data-types/', CustomDeviceDataTypeList.as_view(), name='custom_device-data-type-list'),

path('custom-report/create/', ReportExportCustomizationCreateAPIView.as_view(), name='create-customization'),
path('custom-report/<int:pk>/update/', ReportExportCustomizationUpdateAPIView.as_view(), name='edit-customization'),
path('custom-report/', ReportExportCustomizationListAPIView.as_view(), name='list-customization'),
path('custom-report-IdName/', ReportExportCustomizationIdNameListAPIView.as_view(), name='list-customization-id-name'),
path('custom-report/<int:id>/', ReportExportCustomizationGetAPIView.as_view(), name='get-customization'),
path('custom-report/<int:id>/delete/', ReportExportCustomizationDeleteAPIView.as_view(), name='customization-delete'),


path('landingpage-view/', LandingPageListView.as_view(), name='landing page'),
path('landingpage-vehicle-view/', LandingPageVehicleWiseListView.as_view(), name='landing page vehiicle wise'),


path('service-sheduler/create/', ServiceSchedulerCreateView.as_view(), name='service-sheduler-create'),
path('service-sheduler/update/<int:pk>/', ServiceSchedulerUpdateView.as_view(), name='service-sheduler-update'),
path('service-sheduler/<int:pk>/delete/', ServiceSchedulerDelete.as_view(), name='service-sheduler-delete'),
path('service-sheduler/list/', ServiceSchedulerList.as_view(), name='service-sheduler-list'),


path('geofence/create/', GeofenceCreateView.as_view(), name='Geofence-create'),
path('geofences/<int:pk>/update/', GeofenceUpdateView.as_view(), name='Geofence-update'),
path('geofences/<int:pk>/delete/', GeofenceDeleteView.as_view(), name='geofence-delete'),
path('geofence/list/', GeofenceList.as_view(), name='Geofence-list'),

path('trip/create/', TripCreateView.as_view(), name='trip-create'),
path('trip/<int:pk>/update/', TripUpdateView.as_view(), name='trip-update'),
path('trip/<int:pk>/delete/', TripDeleteView.as_view(), name='trip-delete'),
path('trip/list/', TripList.as_view(), name='trip-list'),
path("trip/<str:trip_id>/", TripDetailView.as_view(), name="trip-detail"),


path('reports/driving-behavior/', DrivingBehaviorReportView.as_view(), name='driving_behavior_report'),
]