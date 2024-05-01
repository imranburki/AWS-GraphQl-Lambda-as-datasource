from typing import Dict

AppSyncEvent = Dict[str, Dict[str, str]]

def lambda_handler(event: AppSyncEvent,context) -> str:
    notes_array = ["note1", "note2", "note3"]

    field_name = event.get("info", {}).get("fieldName")
    arguments = event.get("arguments", {})

    if field_name == "notes":
        return notes_array
    elif field_name == "customNote":
        return arguments.get("title")
    else:
        return None



# def lambda_handler(event, context):
#     message = 'Hello lambda world'  
#     return { 
#         'message' : message
#     }