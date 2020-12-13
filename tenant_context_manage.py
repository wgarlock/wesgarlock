#!/usr/bin/env python
import os
import sys

from wesgarlock.tenant.middleware import set_db_for_router
from wesgarlock.tenant.utils import connect_database

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    from django.db import connection

    args = sys.argv
    db = args[1]

    with connection.cursor() as cursor:
        set_db_for_router(db)
        connect_database(db)
        del args[1]
        execute_from_command_line(args)
