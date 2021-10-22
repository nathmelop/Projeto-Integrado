# Databricks notebook source
pip install importlib_resources


# COMMAND ----------

# MAGIC %scala
# MAGIC //Conector Blob Storage - Databricks
# MAGIC val containerName = "testingstuff"
# MAGIC val storageAccountName = "storageaccountgrupo03"
# MAGIC val sas = "sp=r&st=2021-10-15T21:40:40Z&se=2021-10-16T05:40:40Z&spr=https&sv=2020-08-04&sr=c&sig=spGWs9F25d9KjxPcqy1idyWJGpeaaQPf91jcynnzZE8%3D"
# MAGIC val url = "wasbs://" + containerName + "@" + storageAccountName + ".blob.core.windows.net/"
# MAGIC val config = "fs.azure.sas." + containerName+ "." + storageAccountName + ".blob.core.windows.net"

# COMMAND ----------

# MAGIC %fs ls

# COMMAND ----------



import urllib

url_steambases = {
  # CSV - Arquivos 'acidentes_nao_fatais.csv' e 'obitos.csv' via url
  "applicationgenres":["https://md-datasets-public-files-prod.s3.eu-west-1.amazonaws.com/1b6e7fe3-bdac-4b6e-bfb7-d000393bc7b5", "applicationgenres.csv"],
  "applicationinformation":["https://md-datasets-public-files-prod.s3.eu-west-1.amazonaws.com/84ad95b5-04eb-4c12-9a22-4afd4b9c920e", "applicationinformation.csv"],
  "applicationsupportedlanguages":["https://md-datasets-public-files-prod.s3.eu-west-1.amazonaws.com/b7310212-ac7f-4fb2-b4b6-c4190954122b", "applicationsupportedlanguages.csv"],
  "applicationtags":["https://md-datasets-public-files-prod.s3.eu-west-1.amazonaws.com/32be707f-efb6-4668-9575-bedb22f3003d", "applicationtags.csv"],
    
} 

# CSv -  Envio dos arquivos para o Blob Storage arquivos 
urllib.request.urlretrieve(url_steambases["applicationgenres"][0], "/dbfs/mnt/testingstuff/{}".format(url_steambases["applicationgenres"][1]))
urllib.request.urlretrieve(url_steambases["applicationinformation"][0], "/dbfs/mnt/testingstuff/{}".format(url_steambases["applicationinformation"][1]))
urllib.request.urlretrieve(url_steambases["applicationsupportedlanguages"][0], "/dbfs/mnt/testingstuff/{}".format(url_steambases["applicationsupportedlanguages"][1]))
urllib.request.urlretrieve(url_steambases["applicationtags"][0], "/dbfs/mnt/testingstuff/{}".format(url_steambases["applicationtags"][1]))




# COMMAND ----------

# Importando e extraindo um csv em que na url original está no arquivo zip para o blob.
from urllib.request import urlopen
from zipfile import ZipFile

zipurl = 'https://storage.googleapis.com/kaggle-data-sets/1605661/2673899/compressed/steam_charts.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20211021%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20211021T132407Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=0752d1be0bb0b044f3e31959c8a52cb4493f2f91de621d11de03b8f699871988d94f1ebbeb8610ef9c7d805108ad784687dd0b390e528e4c74494200cbb4775ff14e04eefa902057637c77c27798df15938635e4e9611b7add2c861537d22df2fffb1a7cde930665458a37443f8d01d8a07e8a92d26258533a51753cb2479df8c287229a3a08242d6e2fc7b9cc2a449d9b4e9472875f325ab34c38a236518164db0d96d22f27cf02e37a7d0a80b8be5d12cb4479db37b779c5cf4056de80a1e756a63c31cc927ba7265d137cf88246f2195da31ad476663eba821bbd159000f5efef6c0f6e6e77ba26b2d17bc561f52a8b21e8f8bfce9979abd09b4247d6e532'
    # download do arquivo pela url
zipresp = urlopen(zipurl)
    # cria um novo arquivo no hd
tempzip = open("/tmp/tempfile.zip", "wb")
    # escreve o conteudo do url no arquivo criado no hd
tempzip.write(zipresp.read())
    # fecha o arquivo criado
tempzip.close()
    # reabre o arquivo com ZipFile()
zf = ZipFile("/tmp/tempfile.zip")
    # Extrai o conteudo para o diretorio indicado
zf.extractall(path = '/dbfs/mnt/testingstuff')
    # close the ZipFile instance
zf.close()

# COMMAND ----------

# INSERINDO COLUNAS NO CSV APPTAGS QUE VIERAM SEM HEADER
import pandas as pd
with open("/dbfs/mnt/testingstuff/applicationtags.csv", 'r') as temp_f:
    # Conta o numero de colunas em cada linha
    col_count = [ len(l.split(",")) for l in temp_f.readlines() ]

# Gera um numero de colunas  (colunas serão: 0, 1, 2, ...)
column_names = [i for i in range(0, max(col_count))]

# Lendo o csv
applicationtagsdf = pd.read_csv("/dbfs/mnt/testingstuff/applicationtags.csv", header=None, delimiter=",", names=column_names)

display(applicationtagsdf)

# COMMAND ----------

# Reinserindo o apptags no blob após a inserção de headers

applicationtagsdf.to_csv(r'/dbfs/mnt/testingstuff/applicationtags.csv', index = False)

# COMMAND ----------

# INSERINDO COLUNAS NO CSV APPSUPLANGUAGES QUE VIERAM SEM HEADER

with open("/dbfs/mnt/testingstuff/applicationsupportedlanguages.csv", 'r') as temp_f:
    # get No of columns in each line
    col_count = [ len(l.split(",")) for l in temp_f.readlines() ]

# Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
column_names = [i for i in range(0, max(col_count))]

# Read csv
applicationsupportedlanguagesdf = pd.read_csv("/dbfs/mnt/testingstuff/applicationsupportedlanguages.csv", header=None, delimiter=",", names=column_names)

display(applicationsupportedlanguagesdf)

# COMMAND ----------

applicationsupportedlanguagesdf.to_csv(r'/dbfs/mnt/testingstuff/applicationsupportedlanguages.csv', index = False)

# COMMAND ----------

# INSERINDO COLUNAS NO CSV APPGENRES QUE VIERAM SEM HEADER
import pandas as pd

with open("/dbfs/mnt/testingstuff/applicationgenres.csv", 'r') as temp_f:
    # get No of columns in each line
    col_count = [ len(l.split(",")) for l in temp_f.readlines() ]

# Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
column_names = [i for i in range(0, max(col_count))]

# Read csv
applicationgenresdf = pd.read_csv("/dbfs/mnt/testingstuff/applicationgenres.csv", header=None, delimiter=",", names=column_names)

display(applicationgenresdf)

# COMMAND ----------

applicationgenresdf.to_csv(r'/dbfs/mnt/testingstuff/applicationgenres.csv', index = False)


   