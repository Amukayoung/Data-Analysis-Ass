import json
from questions.models import InlineQuestion


def processInlineQuestionData(filePath):
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            unique_questions = set()
            for item in data:
                for key, value in item.items():
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
                            "ask",
                            "cor",
                        )
                    ):
                        unique_questions.add(key)
                    if key.startswith(("questionKey")):
                        unique_questions.add(value)

            questions_list = []

            for unique_question in unique_questions:
                questions_list.append(InlineQuestion(name=unique_question))

            # Bulk create Question instances
            InlineQuestion.objects.bulk_create(questions_list)

            return f"{len(questions_list)} Unique Questions from JSON file have been saved successfully!"

    except Exception as e:
        return f"Error processing file: {str(e)}"
