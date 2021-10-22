# Databricks notebook source
# MAGIC %sh
# MAGIC pip install steamspypi

# COMMAND ----------

# Importando as bibliotecas necessárias para análise
import json
import time
from pathlib import Path
import pandas as pd
 

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
    # Traz o dia de hoje com o formato yyyyMMdd 
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
    # Criterio para baixar um certo numero de páginas
    data = download_all_pages(num_pages=50)
    df = pd.DataFrame.from_dict(data,'index')
    
del df["score_rank"]
del df["userscore"]
del df["discount"]

df = df.replace(' .. ',' _ ', regex=True)

df['name'] = df['name'].str.replace(',',' ')
df['developer'] = df['developer'].str.replace(',','/')
df['owners'] = df['owners'].str.replace('_','/')
df['owners'] = df['owners'].str.replace(',','.')

pandasDF = df


display(pandasDF)



# COMMAND ----------

# MAGIC %scala
# MAGIC val containerName = "testingstuff"
# MAGIC val storageAccountName = "storageaccountgrupo03"
# MAGIC val sas = "sp=r&st=2021-10-15T21:40:40Z&se=2021-10-16T05:40:40Z&spr=https&sv=2020-08-04&sr=c&sig=spGWs9F25d9KjxPcqy1idyWJGpeaaQPf91jcynnzZE8%3D"
# MAGIC val url = "wasbs://" + containerName + "@" + storageAccountName + ".blob.core.windows.net/"
# MAGIC val config = "fs.azure.sas." + containerName+ "." + storageAccountName + ".blob.core.windows.net"

# COMMAND ----------

# Criação do diretorio via databricks 

# %scala
# dbutils.fs.mount(
 # source = "wasbs://testingstuff@storageaccountgrupo03.blob.core.windows.net/",
  # mountPoint = "/mnt/testingstuff",
  #extraConfigs = Map(config -> sas))

# COMMAND ----------

# Listagem de diretorios conectados ao notebook

%fs ls

# COMMAND ----------

# Conversor do pandas dataframe contendo nossa base retirada da API para formato csv e gravando o mesmo no Blob Storage

pandasDF.to_csv(r'/dbfs/mnt/testingstuff/filesteambase.csv', index = False)