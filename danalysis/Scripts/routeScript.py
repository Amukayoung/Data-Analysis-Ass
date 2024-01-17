import json
from ..models import Route


def processRouteData(filePath):
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            routeSet = set()
            routeList = []

            for item in data:
                _route = item.get("route")
                _destination = item.get("destination", "notspecified")
                destination_state = item.get("destinationState", "notspecified")

                if _route not in routeSet:
                    routeDetail = Route(
                        route=_route,
                        destination=_destination,
                        destinationState=destination_state,
                    )

                    routeSet.add(_route)

                    routeList.append(routeDetail)

            Route.objects.bulk_create(routeList)
            return f"{len(routeList)} Route data from JSON file have been saved successfully!"

    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error processng file: {str(e)}"
