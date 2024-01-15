import json
from .models import Device


def processDeviceData(filePath):
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            deviceSet = set()
            deviceList = []

            for item in data:
                device_id = item.get("deviceId")
                app_version = item.get("appVersion", "STD001")
                device_model = item.get("deviceModel")
                os = item.get("os")
                os_version = item.get("osVersion")

                if device_id not in deviceSet:
                    deviceDetail = Device(
                        id=device_id,
                        appversion=app_version,
                        deviceModel=device_model,
                        os=os,
                        osversion=os_version,
                    )

                    deviceSet.add(device_id)

                    deviceList.append(deviceDetail)

            Device.objects.bulk_create(deviceList)
            return f"{len(deviceList)} Device data from JSON file have been saved successfully!"

    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error processng file: {str(e)}"
