# type: ignore
import pytz
from peewee import CharField, CompositeKey, Field, Model
from playhouse.db_url import connect, register_database
from playhouse.postgres_ext import BinaryJSONField, PostgresqlExtDatabase

register_database(PostgresqlExtDatabase, "postgres", "postgresql")  # needed for JSON support
db = connect("postgres://postgres@localhost:5433/pgml_development")


class UtcTimeField(Field):
    field_type = "timestamptz"

    def db_value(self, value):
        return value and pytz.UTC.normalize(value)

    def python_value(self, value):
        return value and pytz.UTC.normalize(value)


class BaseModel(Model):
    class Meta:
        database = db


class MinutelyDynamicData(BaseModel):
    map = CharField(null=False)
    time = UtcTimeField(null=True)
    dynamic_data = BinaryJSONField()
    report = BinaryJSONField()

    class Meta:
        table_name = "dynamic_data"
        primary_key = CompositeKey("map", "time")
