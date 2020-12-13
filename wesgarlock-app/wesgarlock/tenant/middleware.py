from wesgarlock import db_ctx

from .utils import tenant_db_from_request


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        db = tenant_db_from_request(request)
        db_ctx.set(db)
        response = self.get_response(request)
        return response


def get_current_db_name():
    return db_ctx.get()


def set_db_for_router(db):
    db_ctx.set(db)
