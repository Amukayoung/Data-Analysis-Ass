import json
from ..models import Sector


def processSectorData(filePath):
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            sectorSet = set()
            sectorList = []

            for item in data:
                sectors = item.get("sectors", [])

                for sector_name in sectors:
                    if sector_name not in sectorSet:
                        sectorDetail = Sector(name=sector_name)

                        sectorSet.add(sector_name)
                        sectorList.append(sectorDetail)

            Sector.objects.bulk_create(sectorList)
            return f"{len(sectorList)} Sector data from JSON file have been saved successfully!"

    except Exception as e:
        return f"Error processng file: {str(e)}"
