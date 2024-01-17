from django.shortcuts import render
from django.http import JsonResponse
from .models import Worker, Sector, Organisation, Route, Device
from questions.models import InlineQuestionFeedback
from .serializers import (
    WorkerSerializers,
    SectorSerializers,
    OrganisationSerializers,
    RouteSerializers,
    DeviceSerializers,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime, timedelta


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def device_details_list(request, format=None):
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
def device_details(request, id, format=None):
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


@api_view(["GET"])
def active_users_last_year_grouped_by_month(request, format=None):
    try:
        current_year = datetime.now().year
        current_month = datetime.now().month

        start_date = datetime(current_year - 1, current_month, 1)
        end_date = datetime(current_year, current_month, 1)

        users_last_year = Worker.objects.filter(
            createdAt__gte=start_date, createdAt__lt=end_date
        )

        users_last_year_grouped = (
            users_last_year.annotate(month=ExtractMonth("createdAt"))
            .annotate(year=ExtractYear("createdAt"))
            .values("year", "month")
            .annotate(total_instances=Count("id"))
            .order_by("year", "month")
        )

        return Response(
            {
                "Success": True,
                "Status": 200,
                "data": {"ActiveUsersLastYearGroupedByMonth": users_last_year_grouped},
            }
        )

    except Exception as e:
        return Response({"Error": f"An error occurred: {str(e)}"})


@api_view(["GET"])
def top_routes_last_year(request, format=None):
    try:
        # Get the current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Calculate the start and end dates for the last year
        start_date = datetime(current_year - 1, current_month, 1)
        end_date = datetime(current_year, current_month, 1)

        # Query to get workers instances that occurred last year
        workers_last_year = Worker.objects.filter(
            createdAt__gte=start_date, createdAt__lt=end_date
        )

        # Group by routeId and count occurrences, including route name
        top_routes_last_year = (
            workers_last_year.values("routeId__id", "routeId__route")
            .annotate(total_count=Count("id"))
            .order_by("-total_count")[:5]
        )

        return Response(
            {
                "Success": True,
                "Status": 200,
                "data": {"TopRoutesLastYear": top_routes_last_year},
            }
        )

    except Exception as e:
        return Response({"Error": f"An error occurred: {str(e)}"})


from django.db.models import Count
from django.db.models.functions import ExtractMonth


from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models import Value, IntegerField
from django.db.models import Q
from django.db.models import Case, When


@api_view(["GET"])
def monthly_inline_question_feedback_last_year(request, format=None):
    try:
        all_months = {i: 0 for i in range(1, 13)}

        last_year_data = (
            InlineQuestionFeedback.objects.filter(
                createdAt__year=datetime.now().year - 1
            )
            .annotate(month=ExtractMonth("createdAt"))
            .values("month")
            .annotate(count=Count("id"))
        )

        for entry in last_year_data:
            all_months[entry["month"]] = entry["count"]

        monthly_counts = [
            {"month": month, "count": count} for month, count in all_months.items()
        ]

        return Response(
            {
                "Success": True,
                "Status": 200,
                "data": {
                    "MonthlyInlineQuestionFeedbackLastYear": monthly_counts,
                },
            }
        )
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
