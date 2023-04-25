from databricks.connect import DatabricksSession
from databricks.sdk.core import Config

config = Config(profile = "dbconnect-dev") 
# profile is the Databricks CLI profile name
# you can also pass cluster_id. e.g. config = Config(profile = "dbconnect-dev",cluster_id = "0119-164841-oartlkb5")

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


# Databricks Utilities
# See https://pypi.org/project/databricks-sdk/ for documentation

from databricks.sdk import WorkspaceClient
import base64
w = WorkspaceClient(profile = "dbconnect-dev")
dbutils = w.dbutils


files_in_root = dbutils.fs.ls('/')
print(f'number of files in root: {len(files_in_root)}')

for c in w.clusters.list():
    print(c.cluster_name)