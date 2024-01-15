import json
from datetime import datetime
from django.db import transaction
from .models import Device, Route, Sector, Organisation, Worker


def processWorkerData(filePath):
    try:
        with open(filePath, "r") as file:
            data = json.load(file)

            with transaction.atomic():
                for item in data:
                    device_id = item.get("deviceId")

                    device, created = Device.objects.get_or_create(id=device_id)

                    created_at = datetime.strptime(
                        item["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    updated_at = datetime.strptime(
                        item["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    _route = item.get("route")
                    age = item.get("age", "Notspecified")
                    gender = item.get("gender", "Notspecified")
                    locale = item.get("locale", "Notspecified")
                    organisation_name = item.get("organisation")
                    sectors = item.get("sectors", [])

                    organisation, created = Organisation.objects.get_or_create(
                        name=organisation_name
                    )

                    routes = Route.objects.filter(route=_route)

                    if routes.exists():
                        route = routes.first()
                    else:
                        route = Route.objects.create(route=_route)

                    first_sector_name = sectors[0] if sectors else "agriculture"

                    sector, created = Sector.objects.get_or_create(
                        name=first_sector_name
                    )

                    worker = Worker(
                        deviceId=device,
                        organisationId=organisation,
                        routeId=route,
                        sectorId=sector,
                        age=age,
                        gender=gender,
                        locale=locale,
                        createdAt=created_at,
                        updatedAt=updated_at,
                    )
                    worker.save()

            return "Worker data from JSON file has been saved successfully!"

    except Exception as e:
        return f"Error processing file: {str(e)}"
