import json
from datetime import datetime
from django.db import transaction
from questions.models import Chapter, Question, QuestionFeedback
from .models import Device


def processQuestionData(filePath):
    try:
        with open(filePath, "r") as file:
            data_list = json.load(file)

            with transaction.atomic():
                for data in data_list:
                    device_id = data.get("deviceId")
                    device, _ = Device.objects.get_or_create(id=device_id)

                    created_at = datetime.strptime(
                        data.get("createdAt", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    updated_at = datetime.strptime(
                        data.get("updatedAt", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
                    )

                    for key, value in data.items():
                        if key.startswith(("1_", "2_", "3_")):
                            chapter_number = key
                            chapter = Chapter.objects.get(name=chapter_number)

                            question_key = list(value.keys())[0]
                            question_data = value[question_key]

                            question = Question(chapterId=chapter, name=question_key)
                            question.save()

                            question_feedback = QuestionFeedback(
                                deviceId=device,
                                questionId=question,
                                feedback=question_data.get("wasThisHelpful", ""),
                                createdAt=created_at,
                                updatedAt=updated_at,
                            )
                            question_feedback.save()

            return "Chapter data from JSON file has been saved successfully!"

    except Exception as e:
        return f"Error processing file: {str(e)}"
