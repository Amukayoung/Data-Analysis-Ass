from django.shortcuts import render
from django.http import JsonResponse
from .models import Worker, Sector, Organisation, Route, Device
from .serializers import (
    WorkerSerializers,
    SectorSerializers,
    OrganisationSerializers,
    RouteSerializers,
    DeviceSerializers,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POST"])
def DeviceDetailsList(request, format=None):
    if request.method == "GET":
        DeviceDetail = Device.objects.all()
        serializer = DeviceSerializers(DeviceDetail, many=True)
        return Response(
            {"Success": True, "Status": 200, "data": {"Device": serializer.data}}
        )
    if request.method == "POST":
        serializer = DeviceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def DeviceDetails(request, id, format=None):
    print("id", id)
    try:
        DeviceDetail = Device.objects.get(id=id)
    except Device.DoesNotExist:
        return Response({"Error": "The device Id passed is incorrect"})
    if request.method == "GET":
        serializer = DeviceSerializers(DeviceDetail)
        return Response(
            {"Success": True, "Status": 200, "data": {"Device": serializer.data}}
        )
    elif request.method == "PUT":
        serializer = DeviceSerializers(DeviceDetail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Device deatils Updated Successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        DeviceDetail.delete()
        return Response("Device deleted successfully")
