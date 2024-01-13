from django.contrib import admin
from .models import (
    InlineQuestion,
    InlineQuestionFeedback,
    Chapter,
    Question,
    QuestionFeedback,
)

# Register your models here.

admin.site.register(InlineQuestion)
admin.site.register(InlineQuestionFeedback)
admin.site.register(Chapter)
admin.site.register(Question)
admin.site.register(QuestionFeedback)
