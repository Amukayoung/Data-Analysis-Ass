from django.db import models


class Device(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    appversion = models.CharField(max_length=255, blank=True, null=True)
    deviceModel = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    osversion = models.CharField(max_length=255, blank=True, null=True)


class Route(models.Model):
    id = models.AutoField(primary_key=True)
    route = models.CharField(max_length=255)
    destination = models.CharField(max_length=255, blank=True)
    destinationState = models.CharField(max_length=255, blank=True)


class Sector(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Organisation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    sectors = models.ManyToManyField(Sector)


class Worker(models.Model):
    id = models.AutoField(primary_key=True)
    deviceId = models.ForeignKey(
        Device, on_delete=models.CASCADE, max_length=255, related_name="workers_device"
    )
    organisationId = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        max_length=255,
        related_name="workers_organisation",
    )
    routeId = models.ForeignKey(
        Route, on_delete=models.CASCADE, max_length=255, related_name="workers_route"
    )
    sectorId = models.ForeignKey(
        Sector, on_delete=models.CASCADE, max_length=255, related_name="workers_sector"
    )
    age = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    locale = models.CharField(max_length=255, blank=True)
    createdAt = models.DateTimeField(blank=True)
    updatedAt = models.DateTimeField(blank=True)
