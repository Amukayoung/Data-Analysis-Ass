from django.db import models
from danalysis.models import Device


class InlineQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class InlineQuestionFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    inlineQuestionId = models.ForeignKey(
        InlineQuestion,
        on_delete=models.CASCADE,
        related_name="inline_question_feedback",
    )
    deviceId = models.ForeignKey(Device, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255, blank=True)
    createdAt = models.DateTimeField(blank=True)
    updatedAt = models.DateTimeField(blank=True)


class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    chapterId = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name="question_chapter"
    )
    name = models.CharField(max_length=255)


class QuestionFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    deviceId = models.ForeignKey(Device, on_delete=models.CASCADE)
    questionId = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_feedback"
    )
    feedback = models.CharField(max_length=255)
    createdAt = models.DateTimeField(blank=True)
    updatedAt = models.DateTimeField(blank=True)
