from django.contrib import admin
from .models import Cities,Logs

class CitiesAdmin(admin.ModelAdmin):
    pass

class LogsAdmin(admin.ModelAdmin):
    list_display = ["user","log_date","location","ip_address","resault","response_time","response_state"]

    def user(self,obj):
        return obj.user_id.id

    def location(self,obj):
        return obj.location_id

admin.site.register(Cities,CitiesAdmin)
admin.site.register(Logs,LogsAdmin)
