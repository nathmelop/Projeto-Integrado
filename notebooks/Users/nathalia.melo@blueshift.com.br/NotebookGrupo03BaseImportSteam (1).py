# Databricks notebook source
# MAGIC %sh
# MAGIC pip install steamspypi

# COMMAND ----------

#importando as bibliotecas necessárias para análise
import json
import time
from pathlib import Path
import pandas as pd
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pyspark

import steamspypi


def get_cooldown():
    cooldown = 70  # 1 minuto de cooldown que o site exige, mas 10 segundos para garantir que a página ta sendo puxada

    return cooldown


def get_some_sleep():
    cooldown = get_cooldown()
    print("Sleeping for {} seconds on {}".format(cooldown, time.asctime()))

    time.sleep(cooldown)

    return


def download_a_single_page(page_no=0):
    print("Downloading page={} on {}".format(page_no, time.asctime()))

    data_request = dict()
    data_request["request"] = "all"
    data_request["page"] = str(page_no)

    data = steamspypi.download(data_request)

    return data


def get_file_name(page_no):
    # Traz o dia de hoje com o formato  yyyymmdd 
    date_format = "%Y%m%d"
    current_date = time.strftime(date_format)
    
    file_name = "{}_steamspy_page_{}.json".format(current_date, page_no)

    return file_name


def download_all_pages(num_pages):
    # Download

    for page_no in range(num_pages):
        file_name = get_file_name(page_no)

        if not Path(file_name).is_file():
            page_data = download_a_single_page(page_no=page_no)

            with open(file_name, "w", encoding="utf8") as f:
                json.dump(page_data, f)

            if page_no != (num_pages - 1):
                get_some_sleep()

    # Agregando

    data = dict()

    for page_no in range(num_pages):
        file_name = get_file_name(page_no)

        with open(file_name, "r", encoding="utf8") as f:
            page_data = json.load(f)

            data.update(page_data)

    return data


if __name__ == "__main__":
    # criterio para baixar um certo numero de páginas
    data = download_all_pages(num_pages=2)
    df = pd.DataFrame.from_dict(data,'index')


pandasDF = df



# COMMAND ----------

pandasDF.to_csv(r'/dbfs/mnt/testingstuff/filetest.csv', index = False)

# COMMAND ----------

from pyspark.sql import SparkSession
#Create PySpark SparkSession
spark = SparkSession.builder \
    .master("local[1]") \
    .appName("Grupo03") \
    .getOrCreate()
#Create PySpark DataFrame from Pandas
sparkDF=spark.createDataFrame(pandasDF) 
sparkDF.printSchema()
sparkDF.show()


# COMMAND ----------


import org.apache.spark.sql.functions.col
import org.apache.spark.sql.types.IntegerType

# Convert String to Integer Type
sparkDF.withColumn("salary",col("salary").cast(IntegerType))
sparkDF.withColumn("salary",col("salary").cast("int"))
sparkDF.withColumn("salary",col("salary").cast("integer"))



# COMMAND ----------

containerName = "testingstuff"
storageAccountName = "storageaccountgrupo03"
config = "fs.azure.sas." + containerName+ "." + storageAccountName + ".blob.core.windows.net"

dbutils.fs.mount(
  source = "wasbs://<testingstuff>@<storageaccountgrupo03>.blob.core.windows.net",
  mount_point = "/mnt/<mount-name>",
  extra_configs = {"<config>":dbutils.secrets.get(scope = "<scope-name>", key = "<key-name>")})

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC val containerName = "testingstuff"
# MAGIC val storageAccountName = "storageaccountgrupo03"
# MAGIC val sas = "sp=r&st=2021-10-15T21:40:40Z&se=2021-10-16T05:40:40Z&spr=https&sv=2020-08-04&sr=c&sig=spGWs9F25d9KjxPcqy1idyWJGpeaaQPf91jcynnzZE8%3D"
# MAGIC val url = "wasbs://" + containerName + "@" + storageAccountName + ".blob.core.windows.net/"
# MAGIC val config = "fs.azure.sas." + containerName+ "." + storageAccountName + ".blob.core.windows.net"

# COMMAND ----------

pandasDF.to_csv(r'/dbfs/mnt/testingstuff/filetest.csv', index = False)

# COMMAND ----------

# MAGIC %scala
# MAGIC aggdata.write.option("header", "true").format("com.databricks.spark.csv").save("/mnt/testingstuff/testimportlib.csv")

# COMMAND ----------

def mount_blob(account_name, account_key, container):
  blob_prefix = f"wasbs://{testingstuff}@{storageaccountgrupo03}.blob.core.windows.net/"
  dbutils.fs.mount(
    source = blob_prefix,
    mount_point = f"/mnt/{container}",
    extra_configs = {
      f"fs.azure.account.key.{storageaccountgrupo03}.blob.core.windows.net":sp=r&st=2021-10-15T21:40:40Z&se=2021-10-16T05:40:40Z&spr=https&sv=2020-08-04&sr=c&sig=spGWs9F25d9KjxPcqy1idyWJGpeaaQPf91jcynnzZE8%3D
    }
  )


# COMMAND ----------

# MAGIC %scala
# MAGIC dbutils.fs.mount(
# MAGIC   source = "wasbs://testingstuff@storageaccountgrupo03.blob.core.windows.net/",
# MAGIC   mountPoint = "/mnt/testingstuff",
# MAGIC   extraConfigs = Map(config -> sas))

# COMMAND ----------

import pandas as pd  
from azure.cosmosdb.table.tableservice import TableService  
from azure.cosmosdb.table.models import Entity  
 
list_of_lists = df.values.tolist()  

table_service = TableService(account_name='xxxx', account_key='xxxxx')  
table_service.create_table(table-name)#creating table  
res = setTable(table-name, list_of_lists)#inserting csv to cloud 

# COMMAND ----------

output_blob_folder = "/mnt/testingstuff"



# COMMAND ----------

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

# COMMAND ----------

# MAGIC %fs ls

# COMMAND ----------

first_row_is_header = "true"
DataFrame = spark.read.format('csv').option("header", first_row_is_header).load('/FileStore/tables/testeimportbase.csv')
DataFrame.write.format('delta').saveAsTable("Grupo3.BaseSteam")

display(DataFrame)

# COMMAND ----------

from pyspark.sql.functions import *
import pyspark
first_row_is_header = "true"
DataFrame = spark.read.format('csv').option("header", first_row_is_header).load('/mnt/testingstuff/steam01.csv')


# COMMAND ----------

(dataframe .coalesce(1) .write .mode("overwrite") .option("header", "true") .format("com.databricks.spark.csv") .save(output_blob_folder))



# COMMAND ----------


# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'grupo-03.database.windows.net' 
database = 'Grupo 3' 
username = 'Grupo_03' 
password = 'admin03@' 
cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for SQLAzure};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# Insert Dataframe into SQL Server:
for index, row in df.iterrows():
     cursor.execute("INSERT INTO steambasetabletest (appid,nameapp,developer,publisher,score_rank,positive,negative,userscore,owners,average_forever,average_2weeks,median_forever,median_2weeks,price) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row.appid,row.nameapp,row.developer,row.publisher,row.score_rank,row.positive,row.negative,row.userscore,row.owners,row.average_forever,row.average_2weeks,row.median_forever,row.median_2weeks,row.price)
cnxn.commit()
cursor.close()

# COMMAND ----------

df.to_csv('/dbfs/FileStore/tables/testeimportbase.csv', index=False, encoding='utf-8')