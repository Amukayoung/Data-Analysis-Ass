import json
from datetime import datetime
from django.db import transaction
from questions.models import Chapter, Question, QuestionFeedback
from ..models import Device


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

                            chapter_keys = list(value.keys())
                            for chapter_key in chapter_keys:
                                print("chapter_keys", chapter_key)
                                question_name = chapter_key
                                question_feedback = value[chapter_key]
                                question, _ = Question.objects.get_or_create(
                                    chapterId=chapter, name=question_name
                                )

                                question_feedback = QuestionFeedback(
                                    deviceId=device,
                                    questionId=question,
                                    feedback=question_feedback,
                                    createdAt=created_at,
                                    updatedAt=updated_at,
                                )
                                question_feedback.save()

            return "Chapter data from JSON file has been saved successfully!"

    except Exception as e:
        return f"Error processing file: {str(e)}"
