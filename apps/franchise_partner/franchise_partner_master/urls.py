from django.urls import path
from .views import*

urlpatterns = [
    # Driver URLs
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('drivers/create/', DriverCreateView.as_view(), name='driver-create'),
    path('drivers-update/<uuid:pk>/', DriverUpdateView.as_view(), name='driver-update'),

    # Vehicle URLs
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/create', VehicleCreateView.as_view(), name='vehicle-create'),
    path('vehicles/<uuid:pk>/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('vehicles-by-filter/', VehicleListByFilterView.as_view(), name='vehicle-list-by-filter'),

    # Document URLs
    path('document/<uuid:id>/', DocumentListView.as_view(), name='document-list'),
    path('document/create/', DocumentCreateView.as_view(), name='document-create'),
    path('document/<uuid:pk>/update/', DocumentUpdateView.as_view(), name='document-update'),

    # DocumentType URLs
    path('document-types/', DocumentTypeListView.as_view(), name='document-type-list'),
    path('document-types/create/', DocumentTypeCreateView.as_view(), name='document-type-create'),
    path('document-types/<uuid:pk>/update/', DocumentTypeUpdateView.as_view(), name='document-type-update'),

    # AccountType URLs
    path('account-types/', AccountTypeListView.as_view(), name='account-type-list'),
    path('account-types/create/', AccountTypeCreateView.as_view(), name='account-type-create'),
    path('account-types/<uuid:pk>/update/', AccountTypeUpdateView.as_view(), name='account-type-update'),

    # Account URLs
    path('accounts/', AccountListView.as_view(), name='account-list'),
    path('accounts/create/', AccountCreateView.as_view(), name='account-create'),
    path('accounts/<uuid:pk>/update/', AccountUpdateView.as_view(), name='account-update'),

    # AccountDevice URLs
    path('account-devices/', AccountDeviceListView.as_view(), name='account-device-list'),
    path('account-devices/create/', AccountDeviceCreateView.as_view(), name='account-device-create'),
    path('account-devices/<uuid:pk>/update/', AccountDeviceUpdateView.as_view(), name='account-device-update'),

    # Franchise Client Accounts URL
    path('franchise/<uuid:franchise_id>/client-accounts/', FranchiseClientAccountsListView.as_view(), name='franchise-client-accounts'),
    path('accounts/type/<uuid:account_type_id>/', AccountByTypeListView.as_view(), name='accounts-by-type'),
    
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/account/<uuid:account_id>/', OrderListView.as_view(), name='order-list-by-account'), 
    path('orders/update/<uuid:pk>/', OrderUpdateView.as_view(), name='order-detail'),

    #subscription
    path('subscription/', SubscriptionListView.as_view(), name='order-list'),
    path('subscription/create/', SubscriptionCreateView.as_view(), name='order-create'),
    path('subscription/account/<uuid:account_id>/', SubscriptionListView.as_view(), name='order-list-by-account'), 
    path('subscription/account/<uuid:account_id>/device/<uuid:device_id>/', SubscriptionListView.as_view(), name='order-list-by-account'), 
    path('subscription/update/<uuid:pk>/', SubscriptionUpdateView.as_view(), name='order-detail'),
    path('subscriptionremaing/account/<uuid:account_id>/device/<uuid:device_id>/', SubscriptionRemainingListView.as_view(), name='order-list-by-account'), 
    
    #device feature
    path('device/feature/<uuid:device_id>/', DeviceFeatureList.as_view(), name='device-feature list'),


    #client devices
    path('client/<uuid:client_id>/device/', ClientDeviceList.as_view(), name='device-feature list'),

    path('accounts/confirmed-orders/', ConfirmedDeviceOrderListView.as_view(), name='confirmed-device-orders'),

    path('dashboard', DashboardListView.as_view(), name='dashboard data'),
    
]
