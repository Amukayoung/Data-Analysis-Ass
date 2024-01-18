from django.shortcuts import render
from django.http import JsonResponse
from .models import Worker, Sector, Organisation, Route, Device
from questions.models import InlineQuestionFeedback, QuestionFeedback, InlineQuestion
from .serializers import (
    UserSerializer,
    WorkerSerializers,
    SectorSerializers,
    OrganisationSerializers,
    RouteSerializers,
    DeviceSerializers,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response(
        {
            "token": token.key,
            "user": {
                "username": serializer.data["username"],
                "email": serializer.data["email"],
            },
        }
    )


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
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
        current_year = datetime.now().year
        current_month = datetime.now().month

        start_date = datetime(current_year - 1, current_month, 1)
        end_date = datetime(current_year, current_month, 1)

        workers_last_year = Worker.objects.filter(
            createdAt__gte=start_date, createdAt__lt=end_date
        )

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


@api_view(["GET"])
def unique_age_counts(request, format=None):
    try:
        age_counts = (
            Worker.objects.values("age")
            .annotate(worker_count=Count("id"))
            .order_by("age")
        )

        result = [
            {"age": entry["age"], "worker_count": entry["worker_count"]}
            for entry in age_counts
        ]

        return Response(
            {
                "Success": True,
                "Status": 200,
                "data": {
                    "UniqueAgeCounts": result,
                },
            }
        )
    except Exception as e:
        return Response({"Error": str(e)}, status=500)


def inline_question_feedback_count(request):
    feedback_count = InlineQuestionFeedback.objects.aggregate(total_count=Count("id"))[
        "total_count"
    ]
    return JsonResponse({"total_count": feedback_count})


def active_worker_count(request):
    worker_count = Worker.objects.aggregate(total_count=Count("id"))["total_count"]
    return JsonResponse({"total_count": worker_count})


def chapter_question_feedback_count(request):
    chapter_feedback_count = QuestionFeedback.objects.aggregate(
        total_count=Count("id")
    )["total_count"]
    return JsonResponse({"total_count": chapter_feedback_count})


@api_view(["GET"])
def unique_age_counts(request, format=None):
    try:
        age_counts = (
            Worker.objects.values("age")
            .annotate(worker_count=Count("id"))
            .order_by("age")
        )

        result = [
            {"age": entry["age"], "worker_count": entry["worker_count"]}
            for entry in age_counts
        ]

        return JsonResponse(
            {
                "Success": True,
                "Status": 200,
                "data": {
                    "UniqueAgeCounts": result,
                },
            }
        )
    except Exception as e:
        return JsonResponse({"Error": str(e)}, status=500)


@api_view(["GET"])
def monthly_question_feedback_counts_2023(request):
    try:
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31, 23, 59, 59)

        feedback_counts_2023 = (
            QuestionFeedback.objects.filter(
                createdAt__gte=start_date, createdAt__lte=end_date
            )
            .annotate(month=ExtractMonth("createdAt"))
            .annotate(year=ExtractYear("createdAt"))
            .values("year", "month")
            .annotate(total_feedback=Count("id"))
            .order_by("year", "month")
        )

        return Response(
            {
                "Success": True,
                "Status": 200,
                "data": {"MonthlyQuestionFeedbackCounts2023": feedback_counts_2023},
            }
        )
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def top_answered_questions(request):
    try:
        top_questions = (
            InlineQuestion.objects.annotate(
                feedback_count=Count("inline_question_feedback")
            )
            .order_by("-feedback_count")[:10]
            .values("name", "feedback_count")
        )

        return Response(
            {
                "Success": True,
                "Status": 200,
                "data": {"TopAnsweredQuestions": list(top_questions)},
            }
        )
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def route_devices(request):
    routes_data = Worker.objects.values("routeId__route", "deviceId__id").order_by(
        "routeId__route"
    )

    routes_dict = {}
    for route_data in routes_data:
        route = route_data["routeId__route"]
        device_id = route_data["deviceId__id"]

        if route not in routes_dict:
            routes_dict[route] = []

        routes_dict[route].append(device_id)

    return JsonResponse({"route_devices": routes_dict})


@api_view(["GET"])
def worker_device_created_at(request):
    workers = Worker.objects.values("deviceId__id", "createdAt")
    return Response({"data": workers})


def worker_route_count(request):
    try:
        route_counts = Route.objects.annotate(
            worker_count=Count("workers_route")
        ).order_by("-worker_count")[:12]

        data = {
            "Success": True,
            "Status": 200,
            "data": {
                "WorkerRouteCounts": [
                    {"route": route.route, "worker_count": route.worker_count}
                    for route in route_counts
                ]
            },
        }
        return JsonResponse(data)
    except Exception as e:
        error_data = {"Success": False, "Status": 500, "Error": str(e)}
        return JsonResponse(error_data, status=500)


def organisation_worker_count(request):
    try:
        organisations = Organisation.objects.annotate(
            worker_count=Count("workers_organisation")
        ).order_by("name")

        data = {
            "Success": True,
            "Status": 200,
            "data": {
                "OrganisationWorkerCounts": [
                    {
                        "organisation": organisation.name,
                        "worker_count": organisation.worker_count,
                    }
                    for organisation in organisations
                ]
            },
        }
        return JsonResponse(data)
    except Exception as e:
        error_data = {"Success": False, "Status": 500, "Error": str(e)}
        return JsonResponse(error_data, status=500)
