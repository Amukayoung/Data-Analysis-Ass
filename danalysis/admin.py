from django.contrib import admin
from .models import Device, Route, Sector, Worker, Organisation


admin.site.register(Device)
admin.site.register(Route)
admin.site.register(Sector)
admin.site.register(Worker)
admin.site.register(Organisation)
