import json
from datetime import datetime
from danalysis.models import Device
from questions.models import InlineQuestion, InlineQuestionFeedback


def processInlineQuestionFeedbackData(filePath):
    try:
        with open(filePath, "r") as file:
            data = json.load(file)

            # Iterate through the JSON data
            for item in data:
                # Assuming 'deviceId' is present in your JSON structure
                device_id = item.get("deviceId")

                # Create or get the Device instance
                device, created = Device.objects.get_or_create(id=device_id)

                # Assuming 'createdAt' is present in your JSON structure
                created_at = datetime.strptime(
                    item["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )

                # Iterate through the keys that start with the specified prefixes
                for key in item.keys():
                    if key.startswith(
                        (
                            "sws",
                            "are",
                            "doY",
                            "how",
                            "und",
                            "lab",
                            "did",
                            "cop",
                            "pai",
                            "ask",
                            "pay",
                            "cor",
                        )
                    ):
                        # Create or get the InlineQuestion instance
                        inline_question, created = InlineQuestion.objects.get_or_create(
                            name=key
                        )

                        # Assuming 'updatedAt' is present in your JSON structure
                        updated_at = datetime.strptime(
                            item["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        )

                        # Create InlineQuestionFeedback instance
                        inline_question_feedback = InlineQuestionFeedback(
                            deviceId=device,
                            inlineQuestionId=inline_question,
                            feedback=item[key],
                            createdAt=created_at,
                            updatedAt=updated_at,
                        )
                        inline_question_feedback.save()

            return "InlineQuestionFeedback data from JSON file has been saved successfully!"

    except Exception as e:
        return f"Error processing file: {str(e)}"


# Replace 'your_file_path.json' with the actual path to your JSON file
result = processInlineQuestionFeedbackData("your_file_path.json")
print(result)
