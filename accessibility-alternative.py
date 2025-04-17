from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DoubleType, StructType, StructField, IntegerType, FloatType
from graphframes import GraphFrame
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("DistributedAccessibilityIndex") \
    .config("spark.jars.packages", "graphframes:graphframes:0.8.3-spark3.1-s_2.12") \
    .getOrCreate()

# -------------------------
# Parameters
# -------------------------
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-t"
output_geojson = "accessibility_index.geojson"

region_lat_min = 22.27
region_lat_max = 22.29
region_lon_min = 114.15
region_lon_max = 114.18

# -------------------------
# Load Nodes
# -------------------------
raw_nodes = spark.read.text(nodes_file).rdd.zipWithIndex().filter(lambda x: x[1] > 0)
parsed_nodes = raw_nodes.map(lambda x: (x[1] - 1, *map(float, x[0][0].value.strip().split())))
filtered_nodes = parsed_nodes.filter(lambda x: region_lat_min <= x[1] <= region_lat_max and region_lon_min <= x[2] <= region_lon_max)

nodes_schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("latitude", FloatType(), False),
    StructField("longitude", FloatType(), False)
])
nodes_df = spark.createDataFrame(filtered_nodes, schema=nodes_schema)

# -------------------------
# Load Edges
# -------------------------
raw_edges = spark.read.text(edges_file).rdd
edges = raw_edges.map(lambda x: x[0].value.strip().split()) \
    .filter(lambda x: len(x) == 3) \
    .map(lambda x: (int(x[0]), int(x[1]), float(x[2]))) \
    .filter(lambda x: x[2] > 0)

edges_schema = StructType([
    StructField("src", IntegerType(), False),
    StructField("dst", IntegerType(), False),
    StructField("weight", FloatType(), False)
])
edges_df = spark.createDataFrame(edges, schema=edges_schema)

# -------------------------
# GraphFrame for Shortest Paths
# -------------------------
graph = GraphFrame(nodes_df.selectExpr("id"), edges_df)

# Use nodes in region as landmarks
landmarks = [row.id for row in nodes_df.select("id").toLocalIterator()]
result = graph.shortestPaths(landmarks=landmarks)

# -------------------------
# Compute Accessibility Index
# -------------------------
def compute_accessibility(distances):
    return float(sum(1.0 / d for d in distances.values() if d > 0)) if distances else 0.0

accessibility_udf = udf(compute_accessibility, DoubleType())
accessibility_df = result.withColumn("accessibility_index", accessibility_udf(col("distances")))

# -------------------------
# Join coordinates
# -------------------------
final_df = accessibility_df.join(nodes_df, on="id").select("id", "latitude", "longitude", "accessibility_index")

# -------------------------
# Convert to GeoJSON
# -------------------------
# Collect as Pandas DataFrame (only small filtered region)
pandas_df = final_df.toPandas()
pandas_df["geometry"] = pandas_df.apply(lambda row: Point(row["longitude"], row["latitude"]), axis=1)

gdf = gpd.GeoDataFrame(pandas_df, geometry="geometry", crs="EPSG:4326")
gdf.to_file(output_geojson, driver="GeoJSON")
print(f"✅ Saved: {output_geojson}")
