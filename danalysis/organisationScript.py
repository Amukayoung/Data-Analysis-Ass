import json
from .models import Organisation, Sector


def processOrganisationData(filePath):
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            organisationSet = set()
            organisationList = []

            for item in data:
                organisation_name = item.get("organisation")
                if organisation_name and organisation_name not in organisationSet:
                    organisationSet.add(organisation_name)

                    sector_names = item.get("sectors", [])

                    organisation = Organisation(name=organisation_name)
                    organisation.save()

                    for sector_name in sector_names:
                        sector, _ = Sector.objects.get_or_create(name=sector_name)
                        organisation.sectors.add(sector)
                organisationList.append(organisation)

            return f"{len(organisationList)} Organisation data from JSON file have been saved successfully!"

    except Exception as e:
        return f"Error processing file: {str(e)}"
