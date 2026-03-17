import psutil

def system_stats():
    battery_percent = psutil.sensors_battery().percent
    memory_percent = psutil.virtual_memory().percent
    final_res = {
        "cpu": {
            "percent": psutil.cpu_percent(),
            "count": psutil.cpu_count(),
        },
        "battery": {
            "charge": psutil.sensors_battery()
        },
        "RAM": {
            "available": psutil.virtual_memory().available,
            "used" : psutil.virtual_memory().used,
            "total": psutil.virtual_memory().total,
            "percent": psutil.virtual_memory().percent,
            "free": psutil.virtual_memory().free
        },
        "disk": []
    }
    for i, partition in enumerate( psutil.disk_partitions() ):
        final_res["disk"].append(
            {
                "configuration": {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "type": partition.fstype,
                    "opts": partition.opts,
                },
                "usage": {
                    "total": psutil.disk_usage( partition.device ).total,
                    "percent": psutil.disk_usage( partition.device ).percent,
                    "usage": psutil.disk_usage( partition.device ).used,
                    "free": psutil.disk_usage( partition.device ).free
                }
            }
        )
    return final_res

import json
print( json.dumps( system_stats(), indent=4 ) )