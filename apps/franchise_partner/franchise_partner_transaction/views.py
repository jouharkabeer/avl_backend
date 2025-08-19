from datetime import timedelta
from django.utils.timezone import now
from .models import * 
from .serializer import *
from apps.service_provider.master.views import BaseListView, DeviceDataType, BaseCreateView, BaseUpdateView, generics, BaseDeleteView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import pandas as pd
from datetime import datetime
from typing import Optional
import io
from django.db.models import CharField
from django.db.models.functions import Cast
from django.http import HttpResponse


def filter_sensor_values(data, allowed_types):
    for record in data:
        record['sensor_values'] = [
            sensor for sensor in record.get('sensor_values', [])
            if sensor['data_type_name'] in allowed_types
        ]
    return data


def calculate_time_span(time_span):
    try:
        value, unit = int(time_span.split('_')[0]), time_span.split('_')[1]
        if unit == "hr":
            time_delta = timedelta(hours=value)
        elif unit == "day":
            time_delta = timedelta(days=value)
        elif unit == "month":
            time_delta = timedelta(days=value * 30)
        else:
            return None
        return now() - time_delta
    except (ValueError, IndexError):
        return None


class LatestVehicleDataView(BaseListView):
    serializer_class = ReportTableSerializer

    def get(self, request):

        user = request.user
        account = getattr(user, 'account', None)
        if not account:
            return Response([])
        
        try:
                imei_numbers = AccountDevice.objects.filter(account_id=account.account_id).values_list('imei_no', flat=True).distinct()
                if not imei_numbers:
                    return Response([])
                
                else:
                    query = ReportTable.objects.filter(imei_no__in=imei_numbers).order_by('imei_no', '-created_at').distinct('imei_no')
                    serializer = self.serializer_class(query, many=True)
                    filtered_data = filter_sensor_values(serializer.data, allowed_types=['Longitude', 'Latitude', 'Altitude'])
                    return Response(filtered_data)

        except (ValueError, IndexError):
            return Response([])


class ReportTableListView(BaseListView):
    serializer_class = ReportTableSerializer

    def post(self, request):

        time_span = request.data.get('time_span', None)
        imei = request.data.get('imei', [])
        take = int(request.data.get('take', 25))
        skip = int(request.data.get('skip', 0))
        user = request.user
        account = getattr(user, 'account', None)

        if not account:
            return Response([])

        try:
            if imei:
                imei_exists = AccountDevice.objects.filter(account_id=account.account_id, imei_no__in=imei).exists()
                if not imei_exists:
                    return Response([])
                imei_numbers = imei
            else:
                imei_numbers = AccountDevice.objects.filter(account_id=account.account_id).values_list('imei_no', flat=True).distinct()

            if not imei_numbers:
                return Response([])
        
            if time_span:
                start_time = calculate_time_span(time_span)
                if start_time is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                query = ReportTable.objects.filter(created_at__gte=start_time, imei_no__in=imei_numbers)
            
            else:
                query = ReportTable.objects.filter(imei_no__in=imei_numbers)

            total_count = query.count()
            results = query.order_by('-created_at')[skip:skip + take]
            serializer = self.serializer_class(results, many=True)
            return Response({
                'data': serializer.data,
                'metadata': {
                    'total': total_count,
                    'take': take,
                    'skip': skip
                }
            })
        except (ValueError, IndexError):
            return Response([])


class GpsDataListView(BaseListView):
    serializer_class = ReportTableSerializer

    def post(self, request):
        time_span = request.data.get('time_span', None)
        imei = request.data.get('imei', [])
        user = request.user
        account = getattr(user, 'account', None)

        if not account:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            if imei:
                imei_exists = AccountDevice.objects.filter(account_id=account.account_id, imei_no__in=imei).exists()
                if not imei_exists:
                    return Response([])
                imei_numbers = imei
            else:
                return Response([])

            if not imei_numbers:
                return Response([])
        
            if time_span:
                start_time = calculate_time_span(time_span)
                if start_time is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                query = ReportTable.objects.filter(created_at__gte=start_time, imei_no__in=imei_numbers)
            else:
                query = ReportTable.objects.filter(imei_no__in=imei_numbers)

            results = query.order_by('-created_at')
            serializer = self.serializer_class(results, many=True)

            filtered_data = filter_sensor_values(serializer.data, allowed_types=['Longitude', 'Latitude', 'Movement'])

            return Response({
                'data': filtered_data,
            })
        except Exception as e:
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class MaintenanceCreateView(BaseCreateView):

    def post(self, request):
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceListView(BaseListView):
    model = Maintenance
    serializer_class = MaintenanceSerializer

    
class MaintenanceDeleteView(BaseListView):
    model = Maintenance
   
    
class MaintenanceUpdateView(BaseUpdateView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

 
class CustomDeviceDataTypeList(BaseListView):
    model = DeviceDataType
    serializer_class = CustomDeviceDataTypeSerializer
    
    def get_queryset(self): 
        return DeviceDataType.objects.filter(showdatatype=True)

  
class ReportExportCustomizationCreateAPIView(BaseCreateView):
    serializer_class = ReportExportCustomizationSerializer


class ReportExportCustomizationUpdateAPIView(BaseUpdateView):
    queryset = ReportExportCustomization.objects.all()
    serializer_class = ReportExportCustomizationSerializer


class ReportExportCustomizationListAPIView(BaseListView):
    model = ReportExportCustomization
    serializer_class = ReportExportCustomizationSerializer

    def get_queryset(self):
        user = self.request.user
        account = user.account
        if account:
            # User belongs to a child account
            return ReportExportCustomization.objects.filter(created_by__account=account)
        
        
class ReportExportCustomizationDeleteAPIView(BaseDeleteView):
    model = ReportExportCustomization
    

class ReportExportCustomizationIdNameListAPIView(BaseListView):
    model = ReportExportCustomization
    serializer_class = ReportExportCustomSerializer

    def get_queryset(self):
        user = self.request.user
        account = user.account
        if account:
            # User belongs to a child account
            return ReportExportCustomization.objects.filter(created_by__account=account)

        
class ReportExportCustomizationGetAPIView(generics.RetrieveAPIView):
    queryset = ReportExportCustomization.objects.all()
    serializer_class = ReportExportCustomizationSerializer
    lookup_field = 'id'

        
class LandingPageListView(BaseListView):
    serializer_class = ReportTableSerializer

    def post(self, request):

        time_span = request.data.get('time_span', None)
        imei = request.data.get('imei', [])
        filters = request.data.get('filters', [])
        user = request.user
        account = getattr(user, 'account', None)

        if not account or not filters:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            if imei:
                imei_exists = AccountDevice.objects.filter(account_id=account.account_id, imei_no__in=imei).exists()
                if not imei_exists:
                    return Response([])
                imei_numbers = imei
            else:
                imei_numbers = AccountDevice.objects.filter(account_id=account.account_id).values_list('imei_no', flat=True).distinct()

            if not imei_numbers:
                return Response([])
        
            if time_span:
                start_time = calculate_time_span(time_span)
                if start_time is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                query = ReportTable.objects.filter(created_at__gte=start_time, imei_no__in=imei_numbers)
            
            else:
                query = ReportTable.objects.filter(imei_no__in=imei_numbers)

            total_count = query.count()
            results = query.order_by('-created_at')
            serializer = self.serializer_class(results, many=True)
            filtered_data = filter_sensor_values(serializer.data, allowed_types=filters)
            return Response({
                'data': filtered_data,
                'metadata': {
                    'total': total_count,
                    'timespan': time_span,
                }
            })
        except (ValueError, IndexError):
            return Response([])

        
class LandingPageVehicleWiseListView(BaseListView):
    serializer_class = ReportTableSerializer

    def post(self, request):
        filters = request.data.get('filters', [])
        user = request.user
        account = getattr(user, 'account', None)

        if not account or not filters:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch imei_numbers for the account
            imei_numbers = AccountDevice.objects.filter(account_id=account.account_id).values_list('imei_no', flat=True).distinct()
            if not imei_numbers:
                return Response([])

            # Query for ReportTable data
            query = (
                ReportTable.objects.filter(imei_no__in=imei_numbers)
                .order_by('vehicle_id', '-created_at')
                .distinct('vehicle_id')[:10]
            )

            total_count = query.count()
            serializer = self.serializer_class(query, many=True)

            # Prepare vehicle_id-to-body_type mapping
            vehicle_map = {
                str(vehicle.vehicle_id): vehicle.body_type.vehicle_type_name if vehicle.body_type else None
                    
                for vehicle in Vehicle.objects.annotate(
                    vehicle_id_str=Cast('vehicle_id', output_field=CharField())
                ).filter(vehicle_id_str__in=query.values_list('vehicle_id', flat=True))
            }

            # Update serialized data with body_type
            serialized_data = serializer.data
            for record in serialized_data:
                vehicle_id = record.get('vehicle_id')
                record['body_type'] = vehicle_map.get(vehicle_id, {"id": None, "name": None})

            # Apply filters to data
            filtered_data = filter_sensor_values(serialized_data, allowed_types=filters)

            # Return the response
            return Response({
                'data': filtered_data,
                'metadata': {
                    'total': total_count
                }
            })

        except (ValueError, IndexError) as e:
            return Response([])

        
class ServiceSchedulerCreateView(BaseCreateView):
    serializer_class = ServiceShedulerSerializer


class ServiceSchedulerList(BaseListView):
    model = ServiceScheduler
    serializer_class = ServiceShedulerSerializer

    
class ServiceSchedulerDelete(BaseDeleteView):
    model = ServiceScheduler
    

class ServiceSchedulerUpdateView(BaseUpdateView):
    queryset = ServiceScheduler.objects.all()
    serializer_class = ServiceShedulerSerializer

    
class GeofenceCreateView(BaseCreateView):
    serializer_class = GeofenceSerializer


class GeofenceUpdateView(BaseUpdateView):
    queryset = Geofences.objects.all()
    serializer_class = GeofenceSerializer


class GeofenceList(BaseListView):
    model = Geofences
    serializer_class = GeofenceSerializer     

    
class GeofenceDeleteView(BaseDeleteView):
    model = Geofences


def export_driving_behavior_to_excel(account_id: str,
                                   start_time: datetime,
                                   end_time: datetime,
                                   output_path: Optional[str]=None) -> io.BytesIO:

    query = """
        SELECT * FROM public.get_driving_behavior_counts(%s, %s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [account_id, start_time, end_time])

        columns = [desc[0] for desc in cursor.description]

        results = cursor.fetchall()

    df = pd.DataFrame(results, columns=columns)

    df = df.rename(columns={
        'imeino': 'IMEI Number',
        'licenseplate': 'License Plate',
        'driver': 'Driver Name',
        'harshbrakingcount': 'Harsh Braking Events',
        'harshaccelerationcount': 'Harsh Acceleration Events',
        'harshcorneringcount': 'Harsh Cornering Events',
        'overspeedingcount': 'Overspeeding Events',
        'rapidaccelerationcount': 'Rapid Acceleration Events',
        'idletimeminutes': 'Idle Time (Minutes)'
    })

    if output_path:
        excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    else:
        excel_buffer = io.BytesIO()
        excel_writer = pd.ExcelWriter(excel_buffer, engine='xlsxwriter')

    df.to_excel(excel_writer, sheet_name='Driving Behavior Report', index=False)

    workbook = excel_writer.book
    worksheet = excel_writer.sheets['Driving Behavior Report']

    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4F81BD',
        'font_color': 'white',
        'border': 1
    })

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    for i, column in enumerate(df.columns):
        column_width = max(
            df[column].astype(str).apply(len).max(),
            len(column)
        )
        worksheet.set_column(i, i, column_width + 2)
    
    excel_writer.close()
    
    if output_path:
        return None
    else:
        excel_buffer.seek(0)
        return excel_buffer  


class DrivingBehaviorReportView(generics.GenericAPIView):
            
    def validate_date(self, date_string):
        try:
            return datetime.strptime(date_string, '%Y-%m-%d')
        except (ValueError, TypeError):
            return None
    
    def get_excel_response(self, account_id, start_time, end_time, imei, show_summary, data_type_codes):
        if show_summary:
            excel_buffer = export_driving_behavior_to_excel(
                account_id=account_id,
                start_time=start_time,
                end_time=end_time
            )
        else:
            if imei:
                excel_buffer = export_single_day_driving_behavior_to_excel(
                    imei_list=imei,
                    data_type_codes=data_type_codes,
                    start_time=start_time,
                    end_time=end_time,
                )
            else:
                imei_numbers = list(AccountDevice.objects.filter(account_id=account_id).values_list('imei_no', flat=True).distinct())
        
                excel_buffer = export_single_day_driving_behavior_to_excel(
                    imei_list=imei_numbers,
                    data_type_codes=data_type_codes,
                    start_time=start_time,
                    end_time=end_time,
                )
        filename = f'driving_behavior_report_{datetime.now().strftime("%Y%m%d")}.xlsx'

        response = HttpResponse(
            excel_buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    def post(self, request, *args, **kwargs):

        user = request.user
        account = getattr(user, 'account', None)
        account_id = account.account_id
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        imei = request.data.get('imei', [])
        custom_report = int(request.data.get('custom_report'))
        show_summary = request.data.get('show_summary', False)
        
        # Validate required fields
        if not all([account_id, start_time, end_time]):
            return Response({
                'error': 'Missing required fields. Please provide account_id, start_time, and end_time.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate and convert dates
        valid_start_time = self.validate_date(start_time)
        valid_end_time = self.validate_date(end_time)
        
        if not valid_start_time or not valid_end_time:
            return Response({
                'error': 'Invalid date format. Use YYYY-MM-DD format.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if valid_start_time > valid_end_time:
            return Response({
                'error': 'End time must be after start time.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data_type_codes = ReportExportCustomization.objects.get(id=custom_report).columns
        
            if not isinstance(data_type_codes, list):
                raise ValueError("The 'columns' field must be a list.")
        
            return self.get_excel_response(
                account_id=str(account_id),
                start_time=valid_start_time,
                end_time=valid_end_time,
                imei=imei,
                show_summary=show_summary,
                data_type_codes=data_type_codes
            )
               
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TripCreateView(BaseCreateView):
    serializer_class = TripSerializer


class TripUpdateView(BaseUpdateView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripList(BaseListView):
    model = Trip
    serializer_class = TripSerializer  


class TripDeleteView(BaseDeleteView):
    model = Trip


class TripDetailView(BaseListView):
    model = Trip
    serializer_class = TripSerializer


from typing import List


def export_single_day_driving_behavior_to_excel(imei_list: List[str],
                                                data_type_codes: List[str],
                                   start_time: datetime,
                                   end_time: datetime,
                                   output_path: Optional[str]=None) -> io.BytesIO:

    query = """
        SELECT * FROM public.export_from_report(%s, %s)
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [data_type_codes, imei_list])

        columns = [desc[0] for desc in cursor.description]

        results = cursor.fetchall()
    
    df = pd.DataFrame(results, columns=columns)
    
    if 'meaning' in df.columns and 'value' in df.columns:
        df = df.drop(columns=['vehicle_id', 'batch', 'driver_id'], errors='ignore')
        pivot_df = df.pivot_table(
            index=[
                 'license_plate', 'imei_no',
                 'driver', 'created_at'
            ],
            columns='meaning',
            values='value',
            aggfunc='first'
        ).reset_index()

        # Flatten the columns after pivoting
        pivot_df.columns = [col[0] if isinstance(col, tuple) else col for col in pivot_df.columns]
    else:
        pivot_df = df  # Fallback in case the required columns are missing

    pivot_df = pivot_df.rename(columns={
        'license_plate': 'Vehicle License Plate',
        'imei_no': 'IMEI Number',
        'driver': 'Driver Name',
        'created_at': 'Occured',
        # Add more renaming as needed for other columns based on your data
    })

    if output_path:
        excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    else:
        excel_buffer = io.BytesIO()
        excel_writer = pd.ExcelWriter(excel_buffer, engine='xlsxwriter')

    # Write the pivoted DataFrame to Excel
    pivot_df.to_excel(excel_writer, sheet_name='Driving Behavior Report', index=False)

    # Apply formatting to the Excel file
    workbook = excel_writer.book
    worksheet = excel_writer.sheets['Driving Behavior Report']

    # Format the header row
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4F81BD',
        'font_color': 'white',
        'border': 1
    })

    for col_num, value in enumerate(pivot_df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Adjust column widths for better readability
    for i, column in enumerate(pivot_df.columns):
        column_width = max(
            pivot_df[column].astype(str).apply(len).max(),
            len(column)
        )
        worksheet.set_column(i, i, column_width + 2)

    excel_writer.close()

    if output_path:
        return None
    else:
        excel_buffer.seek(0)
        return excel_buffer 

