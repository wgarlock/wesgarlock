import contextvars

from django.conf import settings

from wesgarlock import db_ctx


def find_db(hints):
    ctx = contextvars.copy_context()
    if "instance" in hints and hints["instance"] is not None and hints["instance"]._state.db is not None:
        db = hints["instance"]._state.db
    elif ctx.get(db_ctx):
        db = ctx[db_ctx]
    else:
        db = settings.DATABASES['default']["NAME"]
    return db


class DatabaseRouter:
    def db_for_read(self, model, **hints):
        return find_db(hints)

    def db_for_write(self, model, **hints):
        return find_db(hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
