from django.contrib import admin
from .models import HouseModel

# Register your models here.
class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_on']

admin.site.register(HouseModel, HouseAdmin)