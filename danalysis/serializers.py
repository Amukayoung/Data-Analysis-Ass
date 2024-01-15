from rest_framework import serializers
from .models import Device, Route, Sector, Organisation, Worker
from questions.models import (
    InlineQuestion,
    InlineQuestionFeedback,
    Chapter,
    Question,
    QuestionFeedback,
)


class DeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "appversion", "deviceModel", "os", "osversion"]
        # read_only_fields = ["id"]


class RouteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ["id", "deviceId", "route", "destination", "destinationState"]


class SectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ["id", "name"]


class OrganisationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ["id", "name", "sectorId"]


class WorkerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = [
            "id",
            "deviceId",
            "organisationId",
            "routeId",
            "sectorId",
            "age",
            "gender",
            "locale",
            "createdAt",
            "updatedAt",
        ]


class InlineQuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = InlineQuestion
        fields = ["id", "name"]


class InlineQuestionFeedbackSerializers(serializers.ModelSerializer):
    class Meta:
        model = InlineQuestionFeedback
        fields = [
            "id",
            "inlineQuestionId",
            "deviceId",
            "feedback",
            "createdAt",
            "updatedAt",
        ]


class ChapterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "name"]


class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "name", "chapterId"]


class QuestionFeedbackSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuestionFeedback
        fields = ["id", "deviceId", "questionId", "feedback", "createdAt", "updatedAt"]
