
# Databricks Connect V2

## Requirements:
* Unity Catalog enabled Workspace
* DBR 13.0 and above
* Python version (minor version must match between the cluster and your local environment)
* The Databricks Connect major and minor package version should match your Databricks Runtime version. 

## Best Practice and Recomendation
* Use Python Virtual Environment (venv or conda). I prefer conda. See comparision [here](https://www.linkedin.com/pulse/why-you-should-configure-python-virtual-environments-conda-helmuth?trk=pulse-article_more-articles_related-content-card#:~:text=in%20your%20browser.-,Conda,package%20manager%20onto%20your%20computer)
* Existing pyspark on your local machine will conflict with Databricks Connect pyspark. You must uninstall before you install databricks connect.


## Steps:

* Step 1 - Setup Python virtual environment on your local machine

_Important_
* Local Python version should match with the DBR Python version. Run (%sh python --version in your cluster)
* The Databricks Connect major and minor package version should match your Databricks Runtime version (e.g. DBR 13.0 cluster requires databricks-connect=13.0.* package)

```bash
$ conda create --name dbconnectv2 python=3.10
$ conda activate dbconnectv2

```


* Step 2 - Install Databricks Connect Client

First, confirm there is no existing pyspark. if found, run `pip3 uninstall pyspark`
```bash
pip3 show pyspark
WARNING: Package(s) not found: pyspark
```
Then, install databricks-connect package
```bash
$ pip3 install --upgrade "databricks-connect==13.0.*"
# --upgrade option upgrades any existing client installation to the specified version.
```


* Step 3 - Configure Connection Properties

You'll need:
* Workspace URL
* Databircks PAT
* Cluster ID
* Cluster Port - typically 443.

  * Step 3.1 - create a databricks configuration profile file `.databrickscfg.` in your home directory

  ```bash
  $ touch ~/.databrickscfg
  # If you are a databricks CLI user, you can skip this step as you'll already have this file. 
  ```

  * Step 3.2 - add the configuration in the configuration profile file. Example configuration is shown below:

  ```
  [dbconnect-dev]
  host       = https://<workspace-instance-name>
  token      = <access-token-value>
  cluster_id = <cluster-id> 
  ```

* Step 4 - Initialize `DatabricksSession`

Create a python file and initialize the `DatabricksSession` as follows:
```bash
touch hello_databricks_connect.py
```
```python
from databricks.connect import DatabricksSession
from databricks.sdk.core import Config

config = Config(profile = "dbconnect-dev")
spark = DatabricksSession.builder.sdkConfig(config).getOrCreate()

```

* Step 5 - Set the environment variable

```bash
export SPARK_REMOTE="sc://<WORKSPACE_URL>:443/;token=<TOKEN>;x-databricks-cluster-id=<CLUSTER_ID>"
```

* Step 6 - Test the connectivity

```
$ pyspark
Python 3.10.11 (main, Apr 20 2023, 13:59:00) [Clang 14.0.6 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 13.0.0
      /_/

Using Python version 3.10.11 (main, Apr 20 2023 13:59:00)
Client connected to the Spark Connect server at xxxxxxxx.cloud.databricks.com:443
SparkSession available as 'spark'.
>>> spark.range(10).show()
+---+
| id|
+---+
|  0|
|  1|
|  2|
|  3|
|  4|
|  5|
|  6|
|  7|
|  8|
|  9|
+---+
```
 

## Visual Studio Code with Python

Steps to setup a a VS Code project

1. create a project dir: `$ mkdir hello_databricks_connect`
2. Activate python virtual environment containing *databricks-connect* package: `$ conda activate dbconnectv2`
3. Open the project directory in VS Code: `$ code .`
4. Set the current Python interpreter to be the one that is referenced from the virtual environment. On the Command Palette (View > Command Palette), type Python: Select Interpreter, and then press Enter.
5. create a `hello_databricks_connect.py` file with the following code:

```python
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
```
6. Click Run

Debugging

* With the Python code file open, set any breakpoints where you want your code to pause while running.
* Click the Run and Debug icon on the sidebar
* Select the Python file you want to debug

For VS Code specific Python code debuging insgtructions, see [here](https://code.visualstudio.com/docs/python/python-tutorial#_configure-and-run-the-debugger)

## Resources

[Databricks Connect V2 Release Notes](https://docs.databricks.com/release-notes/dbconnect/index.html)

[How to get connection details for your Databricks cluster](https://docs.databricks.com/integrations/jdbc-odbc-bi.html#get-connection-details-for-a-cluster)

[Understanding Workspace URL - Instance and ID](https://docs.databricks.com/workspace/workspace-details.html#workspace-instance-names-urls-and-ids)

[Understanding Cluster URL - ID](https://docs.databricks.com/workspace/workspace-details.html#cluster-url-and-id)


[Migrating to the latest Databricks Connect](https://docs.databricks.com/dev-tools/databricks-connect.html#migrate-to-the-latest-databricks-connect)
