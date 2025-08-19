from django.contrib import admin
from .models import (
    AccountType,
    Account,
    DocumentType,
    Document,
    Driver,
    Vehicle,
    AccountDevice,
    Order,
)

class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('account_type_name', 'description')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_by')
    search_fields = ('name', 'email')

class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'document_type', 'uploaded_at')
    search_fields = ('name',)

class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'license_number', 'email')
    search_fields = ('first_name', 'last_name', 'email')

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'license_plate', 'year')
    search_fields = ('make', 'model', 'license_plate')

class AccountDeviceAdmin(admin.ModelAdmin):
    list_display = ('account', 'device', 'serial_no', 'imei_no')
    search_fields = ('serial_no', 'imei_no')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'account', 'device', 'quantity', 'order_status')
    search_fields = ('order_id', 'account__name', 'device__device_name')

admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(AccountDevice, AccountDeviceAdmin)
admin.site.register(Order, OrderAdmin)
