# utils/db_routers.py

class MyAppRouter:
    """
    A router to control all database operations on models in the
    outreach application.
    """

    def db_for_read(self, model, **hints):
        """Point read operations to the appropriate database."""
        if model._meta.app_label == 'outreach':
            return 'outreach_db'
        return None

    def db_for_write(self, model, **hints):
        """Point write operations to the appropriate database."""
        if model._meta.app_label == 'outreach':
            return 'outreach_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == obj2._meta.app_label:
            return 'outreach_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrations only on the specified database."""
        if app_label == 'outreach':
            return db == 'outreach_db'
        return db != 'outreach_db'
