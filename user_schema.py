
def task_serializer_out(user) -> dict:
    return {
        'id':str(user["_id"]),
        'title':user["title"],
        'is_completed':user["is_completed"]
    }

def tasks_serializer_out(users) -> dict:
    return {"tasks": [task_serializer_out(user) for user in users]}

def tasks_ids_serializer(_ids) -> dict:
    _ids = [{"id": str(_id)} for _id in _ids]
    return _ids