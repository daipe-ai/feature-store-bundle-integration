# Databricks notebook source
# MAGIC %run ../app/bootstrap

# COMMAND ----------

import daipe as dp
from box import Box
from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils

# COMMAND ----------

@dp.notebook_function("%featurestorebundle%")
def init_widgets(config: Box, spark: SparkSession, dbutils: DBUtils):
    spark.sql(f"DROP DATABASE IF EXISTS {config.db_name} CASCADE")
    dbutils.fs.rm(config.base_path, recurse=True)
