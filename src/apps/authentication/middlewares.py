from src.apps.authentication.schemas import decode_jwt_token

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


http_methods = {"GET": "view", "POST": "create",
                "PUT": "update", "DELETE": "delete"}


async def check_permissions(request: Request, call_next) -> JSONResponse:
    path = request.scope.get("path").rstrip("/")
    method = request.scope.get("method")
    access_token = request.headers.get("authorization")

    authentication_route = ["/openapi.json", "/docs", "auth",
                            "/hello-world", "/confirm-register", "/favicon.ico"]
    is_allowed_access = False
    for foo in authentication_route:
        if foo in path:
            is_allowed_access = True
            break

    if not is_allowed_access:
        try:
            access_token_decoded = decode_jwt_token(
                access_token.replace("Bearer ", ""))

            action = http_methods.get(method)
            permissions = access_token_decoded.get("permissions")
            allowed_routes = permissions.get(action)

            allowed_routes_default = access_token_decoded.get("allowed_routes")

            allowed_routes_all = allowed_routes + allowed_routes_default

            path_adjusted = "/" + path.split("/")[1]

            if path_adjusted not in allowed_routes_all:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "detail": "User not authorized to access this resource or action."
                    },
                )
        except:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token or expired."},
            )

    response: JSONResponse = await call_next(request)

    return response
