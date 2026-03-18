def success(data=None, message="success", code=0):
    return {"code": code, "message": message, "data": data or {}}, 200


def fail(message="error", code=1, status_code=400, data=None):
    return {
        "code": code,
        "message": message,
        "data": data or {},
    }, status_code
