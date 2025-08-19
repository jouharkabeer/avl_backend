# type: ignore
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.authentication.models import User
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


class BaseListView(generics.ListAPIView):
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.serializer_class is None:
            raise NotImplementedError("You need to provide a serializer_class.")
        user = self.request.user
        if not user.has_permission('is_view'):
            raise PermissionDenied("You do not have permission to view this content.")
        return self.model.objects.filter(is_delete=False)

    
class BaseCreateView(generics.CreateAPIView):
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.serializer_class is None:
            raise NotImplementedError("You need to provide a serializer_class.")      
        user = self.request.user
        if not user.has_permission('is_add'):
            raise PermissionDenied("You do not have permission to add this content.")
        serializer.save(created_by=user)


class BaseUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = None
    queryset = None
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.serializer_class is None:
            raise NotImplementedError("You need to provide a serializer_class.")
        
        user = self.request.user
        if not user.has_permission('is_edit'):
            raise PermissionDenied("You do not have permission to change this content.")
        serializer.save()

        
class BaseDeleteView(APIView):
    model = None
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if self.model is None:
            return Response({"error": "Model not specified."}, status=status.HTTP_400_BAD_REQUEST)
        lookup_value = kwargs.get(self.lookup_field)
        obj = get_object_or_404(self.model, **{self.lookup_field: lookup_value})
        user = self.request.user
        if not user.has_permission('is_delete'):
            raise PermissionDenied("You do not have permission to delete this content.")
        obj.is_delete = True
        obj.save()
        ChangeLog.objects.create(
            model_name=self.model._meta.model_name,
            object_id=obj.pk,
            action='delete',
            is_delete=True,
            edited_by=user,
            changes={},
            edited_at=timezone.now()
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DeviceBrandListView(BaseListView):
    model = DeviceBrand
    serializer_class = DeviceBrandSerializer


class DeviceBrandCreateView(BaseCreateView):
    model = DeviceBrand
    serializer_class = DeviceBrandSerializer


class DeviceBrandUpdateView(BaseUpdateView):
    model = DeviceBrand
    queryset = DeviceBrand.objects.all()
    serializer_class = DeviceBrandSerializer


class DeviceBrandDeleteView(BaseDeleteView):
    model = DeviceBrand


# Specific Views for TicketCategory
class TicketCategoryListView(BaseListView):
    model = TicketCategory
    serializer_class = TicketCategorySerializer


class TicketCategoryCreateView(BaseCreateView):
    model = TicketCategory
    serializer_class = TicketCategorySerializer


class TicketCategoryUpdateView(BaseUpdateView):
    model = TicketCategory
    queryset = TicketCategory.objects.all()
    serializer_class = TicketCategorySerializer


class TicketCategoryDeleteView(BaseDeleteView):
    model = TicketCategory


# Specific Views for TicketSubCategory
class TicketSubCategoryListView(BaseListView):
    model = TicketSubCategory
    serializer_class = TicketSubCategorySerializer


class TicketSubCategoryCreateView(BaseCreateView):
    model = TicketSubCategory
    serializer_class = TicketSubCategorySerializer


class TicketSubCategoryUpdateView(BaseUpdateView):
    model = TicketSubCategory
    queryset = TicketSubCategory.objects.all()
    serializer_class = TicketSubCategorySerializer


class TicketSubCategoryDeleteView(BaseDeleteView):
    model = TicketSubCategory


# Specific Views for DeviceType
class DeviceTypeListView(BaseListView):
    model = DeviceType
    serializer_class = DeviceTypeSerializer


class DeviceTypeCreateView(BaseCreateView):
    model = DeviceType
    serializer_class = DeviceTypeSerializer


class DeviceTypeUpdateView(BaseUpdateView):
    model = DeviceType
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceTypeDeleteView(BaseDeleteView):
    model = DeviceType


# Specific Views for VehicleType
class VehicleTypeListView(BaseListView):
    model = VehicleType
    serializer_class = VehicleTypeSerializer


class VehicleTypeCreateView(BaseCreateView):
    model = VehicleType
    serializer_class = VehicleTypeSerializer


class VehicleTypeUpdateView(BaseUpdateView):
    model = VehicleType
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer


class VehicleTypeDeleteView(BaseDeleteView):
    model = VehicleType


# Specific Views for DeviceSensor
class DeviceSensorListView(BaseListView):
    model = DeviceSensor
    serializer_class = DeviceSensorSerializer


class DeviceSensorCreateView(BaseCreateView):
    model = DeviceSensor
    serializer_class = DeviceSensorSerializer


class DeviceSensorUpdateView(BaseUpdateView):
    model = DeviceSensor
    queryset = DeviceSensor.objects.all()
    serializer_class = DeviceSensorSerializer


class DeviceSensorDeleteView(BaseDeleteView):
    model = DeviceSensor


# Specific Views for VehiclePlateType
class VehiclePlateTypeListView(BaseListView):
    model = VehiclePlateType
    serializer_class = VehiclePlateTypeSerializer


class VehiclePlateTypeCreateView(BaseCreateView):
    model = VehiclePlateType
    serializer_class = VehiclePlateTypeSerializer


class VehiclePlateTypeUpdateView(BaseUpdateView):
    model = VehiclePlateType
    queryset = VehiclePlateType.objects.all()
    serializer_class = VehiclePlateTypeSerializer


class VehiclePlateTypeDeleteView(BaseDeleteView):
    model = VehiclePlateType


# Specific Views for Device Feature
class DeviceFeatureListView(BaseListView):
    model = DeviceFeature
    serializer_class = DeviceFeatureSerializer


class DeviceFeatureCreateView(BaseCreateView):
    model = DeviceFeature
    serializer_class = DeviceFeatureSerializer


class DeviceFeatureUpdateView(BaseUpdateView):
    model = DeviceFeature
    queryset = DeviceFeature.objects.all()
    serializer_class = DeviceFeatureSerializer


class DeviceFeatureDeleteView(BaseDeleteView):
    model = DeviceFeature


# Specific Views for Device
class DeviceListView(BaseListView):
    model = Device
    serializer_class = DeviceSerializer


class DeviceCreateView(BaseCreateView):
    model = Device
    serializer_class = DeviceSerializer


class DeviceUpdateView(BaseUpdateView):
    model = Device
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDeleteView(BaseDeleteView):
    model = Device


# Specific Views for Unit
class UnitListView(BaseListView):
    model = Unit
    serializer_class = UnitSerializer


class UnitCreateView(BaseCreateView):
    model = Unit
    serializer_class = UnitSerializer


class UnitUpdateView(BaseUpdateView):
    model = Unit
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UnitDeleteView(BaseDeleteView):
    model = Unit


class DeviceDataTypeListView(BaseListView):
    model = DeviceDataType
    serializer_class = DeviceDataTypeSerializer

    def get_queryset(self):

    # Return the filtered queryset
        return DeviceDataType.objects.filter(showdatatype=True)


class DeviceDataTypeCreateView(BaseCreateView):
    model = DeviceDataType
    serializer_class = DeviceDataTypeSerializer


class DeviceDataTypeUpdateView(BaseUpdateView):
    model = DeviceDataType
    queryset = DeviceDataType.objects.all()
    serializer_class = DeviceDataTypeSerializer
