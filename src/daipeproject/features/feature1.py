# Databricks notebook source
# MAGIC %run ../app/bootstrap

# COMMAND ----------

import daipe as dp
import datetime as dt
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from featurestorebundle import time_windows as tw

# COMMAND ----------

@dp.notebook_function()
def init_widgets(widgets_factory: dp.fs.WidgetsFactory):
    widgets_factory.create()

# COMMAND ----------

entity = dp.fs.get_entity()
feature = dp.fs.feature_decorator_factory.create(entity)

# COMMAND ----------

@dp.transformation(display=False)
def load_data(spark: SparkSession):
    return spark.createDataFrame(
        [
            [1, dt.datetime(2022, 1, 1), 100],
            [2, dt.datetime(2022, 1, 1), 200],
        ],
        ["id", "process_date", "feature1"]
    )

# COMMAND ----------

@dp.transformation(
    dp.fs.with_timestamps(
        load_data,
        entity,
        "process_date"
    ),
    display=False
)
def data_with_timestamps(df: DataFrame):
    return df

# COMMAND ----------

@dp.transformation(
    tw.make_windowed(
        data_with_timestamps,
        entity,
        "process_date",
    ),
    display=False
)
def data_with_time_windows(wdf: tw.WindowedDataFrame):
    return wdf

# COMMAND ----------

@dp.transformation(data_with_time_windows, display=False)
@feature(
   dp.fs.Feature(
       "feature1",
       "feature1 description",
       fillna_with=0
   ),
)
def feature1(wdf: tw.WindowedDataFrame):
    return wdf.select("id", "timestamp", "feature1")
