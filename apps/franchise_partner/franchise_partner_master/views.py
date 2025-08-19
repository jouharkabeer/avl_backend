
import json
from django.db import connection
from django.http import Http404
from django.shortcuts import get_object_or_404
from requests import Response
from django.db.models import Sum
from rest_framework import generics
from .models import Driver, Vehicle, DocumentType, AccountType, Account, AccountDevice
from .serializer import *
from apps.service_provider.master.views import BaseCreateView, BaseDeleteView, BaseListView, BaseUpdateView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

# Driver Views
class DriverCreateView(BaseCreateView):
    serializer_class = DriverSerializer

class DriverUpdateView(BaseUpdateView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class DriverListView(BaseListView):
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer
    def get_queryset(self):
        user = self.request.user
        account = user.account
        if account.parent_account:
            return Driver.objects.filter(account=account.account_id)
        client_accounts = Account.objects.filter(parent_account=account)
        return Driver.objects.filter(account__in=client_accounts)

# Document Views
class DocumentCreateView(BaseCreateView):
    serializer_class = DocumentSerializer

class DocumentUpdateView(BaseUpdateView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentListView(BaseListView):
    serializer_class = DocumentSerializer
    def get_queryset(self):
        object_id = self.kwargs.get('id')
        if Document.objects.filter(driver_id=object_id).exists():
            return Document.objects.filter(driver_id=object_id)
        elif Document.objects.filter(vehicle_id=object_id).exists():
            return Document.objects.filter(vehicle_id=object_id)
        else:
            raise Http404("No documents found for the given ID.")

# Vehicle Views
class VehicleCreateView(BaseCreateView):
    serializer_class = VehicleSerializer

class VehicleUpdateView(BaseUpdateView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleListView(BaseListView):
    model = Vehicle
    serializer_class = VehicleListSerializer

    def get_queryset(self):
        user = self.request.user
        account = user.account
        
        if account.parent_account:
            return Vehicle.objects.filter(account=account)
        client_accounts = Account.objects.filter(parent_account=account)
        return Vehicle.objects.filter(account__in=client_accounts)

# DocumentType Views
class DocumentTypeListView(BaseListView):
    model = DocumentType
    serializer_class = DocumentTypeSerializer

class DocumentTypeCreateView(BaseCreateView):
    serializer_class = DocumentTypeSerializer

class DocumentTypeUpdateView(BaseUpdateView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

# AccountType Views
class AccountTypeListView(BaseListView):
    model = AccountType
    serializer_class = AccountTypeSerializer

class AccountTypeCreateView(BaseCreateView):
    serializer_class = AccountTypeSerializer

class AccountTypeUpdateView(BaseUpdateView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

# Account Views
class AccountListView(BaseListView):
    model = Account
    serializer_class = AccountSerializer

class AccountCreateView(BaseCreateView):
    serializer_class = AccountSerializer

class AccountUpdateView(BaseUpdateView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

# AccountDevice Views
class AccountDeviceListView(BaseListView):
    model = AccountDevice
    serializer_class = AccountDeviceSerializer
    def get_queryset(self):
        user = self.request.user
        account = user.account
        if account.parent_account is None:
            child_accounts = Account.objects.filter(parent_account=account).values_list('account_id',flat=True)      
            return AccountDevice.objects.filter(account_id__in=child_accounts)
        return AccountDevice.objects.none()


class AccountDeviceCreateView(BaseCreateView):
    serializer_class = AccountDeviceSerializer

class AccountDeviceUpdateView(BaseUpdateView):
    queryset = AccountDevice.objects.all()
    serializer_class = AccountDeviceSerializer

class FranchiseClientAccountsListView(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        franchise_id = self.kwargs['franchise_id']
        return Account.objects.filter(parent_account=franchise_id)
    
class AccountByTypeListView(generics.ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        account_type_id = self.kwargs['account_type_id']
        return Account.objects.filter(account_type_id=account_type_id)

class AccountDeviceUpdateView(BaseUpdateView):
    queryset = AccountDevice.objects.all()
    serializer_class = AccountDeviceSerializer
    

# List View
class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer

# Create View
class OrderCreateView(BaseCreateView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Detail View (same as before)
class OrderUpdateView(BaseUpdateView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class OrderListView(BaseListView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        account_id = self.kwargs.get('account_id') 
        if account_id:
            return Order.objects.filter(account_id=account_id)  
        return Order.objects.all()
        

class DeviceFeatureList(generics.ListAPIView):
    serializer_class = DevicefeatureSerializer

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        return Device.objects.filter(device_id=device_id)

class ClientDeviceList(generics.ListAPIView):
    serializer_class = AccountDeviceSerializer

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        return AccountDevice.objects.filter(account_id=client_id)
    
class ConfirmedDeviceOrderListView(BaseListView):
    serializer_class = DeviceOrderSerializer

    def get_queryset(self):
        account_id = self.request.user.account
        return (
             Order.objects
        .filter(account_id=account_id, order_status='confirmed')
        .values('device__device_id', 'device__device_name')  # No aliases here
        .annotate(total_quantity=Sum('quantity'))
        )


class DashboardListView(generics.ListAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        account = user.account
        filters = json.dumps(request.data.get('filters'))
        if account and account.parent_account is None:
            # Case 1: Root account (no parent account)
            child_accounts = Account.objects.filter(parent_account=account)
            account_type = account.account_type.account_type_name
            vehicle_count = Vehicle.objects.filter(account_id__in=child_accounts.values_list('account_id', flat=True)).count()
            device_count = AccountDevice.objects.filter(account_id__in=child_accounts.values_list('account_id', flat=True)).count()
            account_count = child_accounts.count()

            data = {
                "account_type": account_type, 
                "device_count": device_count,
                "vehicle_count": vehicle_count,
                "account_count": account_count,
            }
            if filters:
                sensor_counts = get_calculated_sensor_counts(account.account_id, filters)
                data['sensor_counts'] = sensor_counts

        elif account and account.parent_account is not None:
            # Case 2: Child account (has a parent account)
            account_type = account.account_type.account_type_name
            vehicle_count = Vehicle.objects.filter(account_id=account.account_id).count()
            device_count = AccountDevice.objects.filter(account_id=account.account_id).count()

            data = {
                "account_type": account_type,
                "device_count": device_count,
                "vehicle_count": vehicle_count,
            }

            # Call get_calculated_sensor_counts function for this account
            if filters:
                sensor_counts = get_calculated_sensor_counts(account.account_id, filters)
                data['sensor_counts'] = sensor_counts

        else:
            # Case 3: No account associated (service provider logic)
            account_type = "Service Provider"
            vehicle_count = Vehicle.objects.filter(status=True).count()
            device_count = AccountDevice.objects.filter(status=True).count()
            account_count = Account.objects.filter(parent_account=None).count()

            data = {
                "account_type": account_type,
                "device_count": device_count,
                "vehicle_count": vehicle_count,
                "client_account_count": account_count,
            }

        return Response(data)

def filter_vehicle_data(vehicles, filters):
    vehicle_data = []

    for vehicle in vehicles:
        vehicle_dict = {}

        for field in filters:
            if hasattr(vehicle, field):
                vehicle_dict[field] = getattr(vehicle, field)

        if "imei_no" in filters:

            imei = AccountDevice.objects.filter(account_id=vehicle.account_id, vehicle_id = vehicle.vehicle_id
            ).values_list("imei_no", flat=True).first()
            vehicle_dict["imei_no"] = imei

        if vehicle_dict:
            vehicle_data.append(vehicle_dict)

    return vehicle_data
    
from rest_framework import status
class VehicleListByFilterView(BaseListView):
    serializer_class = VehicleListSerializer

    def post(self, request):
        user = request.user
        account = user.account
        filters = request.data.get('filters', [])

        if not account or not filters:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if account.parent_account:  # Child account
            vehicles = Vehicle.objects.filter(account=account)
        else:  
            client_accounts = Account.objects.filter(parent_account=account)
            vehicles = Vehicle.objects.filter(account__in=client_accounts)

        vehicle_data = filter_vehicle_data(vehicles, filters)
        return Response({"vehicles": vehicle_data,})

def get_calculated_sensor_counts(account_id, filters):
    # Execute the PostgreSQL function and fetch the results
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM public.get_calculated_sensor_counts(%s ::text, %s);
            """,
            [account_id, filters]
        )
        results = cursor.fetchall()
        sensor_counts = {row[0]: row[1] for row in results}
    return sensor_counts


# List View
class SubscriptionListView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

# Create View
class SubscriptionCreateView(BaseCreateView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

# Detail View (same as before)
class SubscriptionUpdateView(BaseUpdateView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    
class SubscriptionListView(BaseListView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        account_id = self.kwargs.get('account_id') 
        device_id = self.kwargs.get('device_id')
        if account_id and device_id:
            return Subscription.objects.filter(account_id=account_id, device_id=device_id)
        elif account_id:  
            return Subscription.objects.filter(account_id=account_id)  
        return Subscription.objects.all()

# class SubscriptionfilteredListView(BaseListView):
#     serializer_class = SubscriptionSerializer

#     def get_queryset(self):
#         account_id = self.kwargs.get('account_id') 
#         device_id = self.kwargs.get('device_id')
#         if account_id and device_id:
#             return Order.objects.filter(account_id=account_id, device_id=device_id)  
#         return Order.objects.all()


from django.db.models import Count, F
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subscription  # Ensure the correct import for your model

# class SubscriptionRemainingListView(APIView):
#     def get(self, request, *args, **kwargs):
#         account_id = self.kwargs.get('account_id')
#         device_id = self.kwargs.get('device_id')

#         # Fetch subscriptions matching account_id and device_id
#         queryset = Subscription.objects.filter(account_id=account_id, device_id=device_id).values('subscription_id', 'count')
#         for subscription in queryset:
#             subscription_count = Count (AccountDevice.objects.filter(subscription_id = subscription))
#             if subscription_count - count > 0:
#                 data = list(subscription)
#         # Convert queryset to a list
#         return Response(data)  # Return JSON response


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Subscription, AccountDevice

class SubscriptionRemainingListView(APIView):
    def get(self, request, *args, **kwargs):
        account_id = self.kwargs.get('account_id')
        device_id = self.kwargs.get('device_id')

        # Fetch subscriptions matching account_id and device_id
        queryset = Subscription.objects.filter(account_id=account_id, device_id=device_id).values('subscription_id','subscription_name', 'count')
        
        data = []  # Initialize an empty list to store valid subscriptions

        for subscription in queryset:
            subscription_id = subscription['subscription_id']
            
            subscription_count = AccountDevice.objects.filter(subscription_id=subscription_id).count()
            if subscription['count'] - subscription_count > 0:
                subscription['remaning_count'] = subscription['count'] - subscription_count
                data.append(subscription)
                #data.append(Subscription.objects.filter(subscription_id = subscription_id))  # Append valid subscriptions to data list

        return Response(data)

    

        # queryset = Subscription.objects.subscripion_id.filter(account_id=account_id, device_id=device_id)
        # if account_id and device_id:
        #     queryset = queryset.filter(account_id=account_id, device_id=device_id)
        # elif account_id:
        #     queryset = queryset.filter(account_id=account_id)

        # # Annotate with the count of related AccountDevice entries
        # subscriptions = queryset.annotate(
        #     used_count=Count('AccountDevice')
        # ).annotate(
        #     remaining=F('count') - F('used_count')  # Calculate remaining credits
        # ).filter(remaining__gt=0)  # Only include subscriptions with remaining credits

        # serializer = SubscriptionSerializer(subscriptions, many=True)
        # return Response(serializer.data)
