from typing import Union, List
from fastapi import Request, APIRouter
from starlette.responses import PlainTextResponse
import re


def get_regex_from_path(path: str):
    return re.sub(r"\{[a-zA-Z_-]+\}", r"[^/]+", path)


APIRouter.__hash__ = lambda self: id(self)


class CORSMiddleware:
    routers = {}

    def __init__(
        self,
        router: APIRouter,
        origins: Union[List[str], str] = [],
        allow_credentials: bool = False,
        max_age: int = 86400,
    ):
        self.router = router
        self.path = None
        if router not in CORSMiddleware.routers:
            CORSMiddleware.routers[router] = {
                "origins": origins,
                "allow_credentials": allow_credentials,
                "max_age": max_age,
                "endpoints": {},
            }

    @property
    def endpoints(self):
        return CORSMiddleware.routers[self.router]["endpoints"]

    def set_path(self, path: str):
        self.path = path
        self.regex_path = get_regex_from_path(path)
        if self.regex_path not in self.endpoints:
            self.endpoints[self.regex_path] = {
                "origins": CORSMiddleware.routers[self.router]["origins"],
                "methods": [],
                "headers": [],
                "expose_headers": [],
                "allow_credentials": CORSMiddleware.routers[self.router][
                    "allow_credentials"
                ],
                "max_age": CORSMiddleware.routers[self.router]["max_age"],
                "defined": False,
            }
        return self

    def allow_origin(self, origin: str):
        if origin == "*":
            self.endpoints[self.regex_path]["origins"] = "*"
        else:
            self.endpoints[self.regex_path]["origins"].append(origin)
        return self

    def allow_origins(self, *origins: str):
        self.endpoints[self.regex_path]["origins"] = origins
        return self

    def allow_header(self, header: str):
        self.endpoints[self.regex_path]["headers"].append(header.lower())
        return self

    def allow_headers(self, *headers: str):
        self.endpoints[self.regex_path]["headers"] = [h.lower() for h in headers]
        return self

    def expose_header(self, header: str):
        self.endpoints[self.regex_path]["expose_headers"].append(header.lower())
        return self

    def expose_headers(self, *headers: str):
        self.endpoints[self.regex_path]["expose_headers"] = [h.lower() for h in headers]
        return self

    def allow_method(self, method: str):
        self.endpoints[self.regex_path]["methods"].append(method.upper())
        return self

    def allow_methods(self, methods: List[str]):
        self.endpoints[self.regex_path]["methods"] = [m.lower() for m in methods]
        return self

    def allow_credentials(self, value: bool):
        self.endpoints[self.regex_path]["allow_credentials"] = value
        return self

    def set_max_age(self, value: int):
        self.endpoints[self.regex_path]["max_age"] = value
        return self

    def setup_router(self, method):
        if self.endpoints[self.regex_path]["defined"]:
            return method

        path = str(self.regex_path)

        async def cors_preflight(request: Request):
            requested_method = request.headers.get("Access-Control-Request-Method")
            requested_headers = request.headers.get("Access-Control-Request-Headers")
            if requested_method is None:
                return PlainTextResponse("Disallowed CORS", status_code=400, headers={})
            failures = []
            origin = request.headers.get("Origin")
            response_headers = {
                "Access-Control-Allow-Credentials": "true"
                if self.endpoints[path]["allow_credentials"]
                else "false",
                "Access-Control-Allow-Methods": ", ".join(
                    self.endpoints[path]["methods"]
                ),
                "Access-Control-Max-Age": str(self.endpoints[path]["max_age"]),
            }
            if not origin or path is None:
                failures.append("origin")

            if requested_method not in self.endpoints[path]["methods"]:
                failures.append("method")
            if (
                self.endpoints[path]["headers"]
                and self.endpoints[path]["headers"] != "*"
            ):
                response_headers["Access-Control-Allow-Headers"] = ", ".join(
                    self.endpoints[path]["headers"]
                )
            if self.endpoints[path]["methods"] == "*" and requested_headers is not None:
                response_headers["Access-Control-Allow-Headers"] = requested_headers
            elif requested_headers is not None:
                for header in [h.lower() for h in requested_headers.split(",")]:
                    if header.strip() not in self.endpoints[path]["headers"]:
                        failures.append("headers")
                        break

            if self.endpoints[path]["expose_headers"]:
                response_headers["Access-Control-Expose-Headers"] = ", ".join(
                    self.endpoints[path]["expose_headers"]
                )
            if (
                self.endpoints[path]["allow_credentials"]
                or self.endpoints[path]["origins"] == "*"
            ):
                response_headers["Vary"] = "Origin"
            if (
                origin in self.endpoints[path]["origins"]
                or self.endpoints[path]["origins"] == "*"
            ):
                response_headers["Access-Control-Allow-Origin"] = origin
            if failures:
                return PlainTextResponse(
                    f"Disallowed CORS {', '.join(failures)}",
                    status_code=400,
                    headers=response_headers,
                )
            else:
                return PlainTextResponse(
                    "OK", status_code=200, headers=response_headers
                )

        @self.router.options(f"/{self.path}")
        async def cors_preflight_route(request: Request):
            return await cors_preflight(request)

        self.endpoints[self.regex_path]["defined"] = True
        return method

    def get(self, *args, **kwargs):
        self.allow_method("GET")
        return self.setup_router(self.router.get(f"/{self.path}", *args, **kwargs))

    def post(self, *args, **kwargs):
        self.allow_method("POST")
        return self.setup_router(self.router.post(f"/{self.path}", *args, **kwargs))

    def patch(self, *args, **kwargs):
        self.allow_method("PATCH")
        return self.setup_router(self.router.patch(f"/{self.path}", *args, **kwargs))

    def put(self, *args, **kwargs):
        self.allow_method("PUT")
        return self.setup_router(self.router.put(f"/{self.path}", *args, **kwargs))

    def delete(self, *args, **kwargs):
        self.allow_method("DELETE")
        return self.setup_router(self.router.delete(f"/{self.path}", *args, **kwargs))
