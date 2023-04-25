from databricks.connect import DatabricksSession
from databricks.sdk.core import Config

config = Config(profile = "dbconnect-dev")
spark = DatabricksSession.builder.sdkConfig(config).getOrCreate()

df = spark.read.table("samples.nyctaxi.trips")
schema = df.schema
all_columns = [col.name for col in schema]
number_of_columns = len(all_columns)
numeric_columns = [col.name for col in schema if col.dataType.typeName() in ["integer", "double", "float", "long", "decimal"]]

longer_trips = df.filter(df.trip_distance > 10)
longer_trips_count = longer_trips.count()
print("Total number of columns: " + str(number_of_columns))
print("Total number of longer trips: " + str(longer_trips_count))
