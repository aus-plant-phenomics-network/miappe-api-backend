from litestar import get
from litestar.handlers import HTTPRouteHandler
from typing import Callable


def create_get_handler(
    fn: Callable, params_t: dict[str, type], return_t: type, **kwargs
) -> HTTPRouteHandler:
    for param, t in params_t.items():
        fn.__annotations__[param] = t
    fn.__annotations__["return"] = return_t
    return get(**kwargs)(fn)
