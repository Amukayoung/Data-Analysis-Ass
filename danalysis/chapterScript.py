import json
from questions.models import Chapter


def processChapterData(filePath):
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            chapter_set = set()

            for item in data:
                for key in item:
                    if key.startswith(("1_", "2_", "3_")):
                        chapter_number = key
                        if chapter_number not in chapter_set:
                            chapter_set.add(chapter_number)
                            chapter = Chapter(name=chapter_number)
                            chapter.save()

            return f"{len(chapter_set)} Chapter numbers from JSON file have been saved successfully!"

    except Exception as e:
        return f"Error processing file: {str(e)}"
