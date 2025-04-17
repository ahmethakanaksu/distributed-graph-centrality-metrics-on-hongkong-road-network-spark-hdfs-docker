from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, udf, struct
from pyspark.sql.types import *
from shapely.geometry import Point
import geojson

# Initialize Spark Session
spark = SparkSession.builder.appName("DistributedBetweennessCentrality").getOrCreate()
sc = spark.sparkContext

# Parameters
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d"
output_geojson = "betweenness_centrality.geojson"

# Region bounding box
region_lat_min, region_lat_max = 22.27, 22.29
region_lon_min, region_lon_max = 114.15, 114.18

# Load and filter nodes
nodes_rdd = spark.read.text(nodes_file).rdd.zipWithIndex().filter(lambda x: x[1] > 0)
nodes_filtered = (
    nodes_rdd.map(lambda x: (x[1] - 1, x[0][0].strip().split()))
              .filter(lambda x: len(x[1]) == 2)
              .map(lambda x: (int(x[0]), float(x[1][0]), float(x[1][1])))
              .filter(lambda x: region_lat_min <= x[1] <= region_lat_max and region_lon_min <= x[2] <= region_lon_max)
)

nodes_df = nodes_filtered.toDF(["nodeID", "latitude", "longitude"])
region_node_ids = [row["nodeID"] for row in nodes_df.collect()]
region_node_ids_bc = sc.broadcast(set(region_node_ids))

# Load and filter edges
edges_rdd = spark.read.text(edges_file).rdd.zipWithIndex().filter(lambda x: x[1] > 0)
edges_filtered = (
    edges_rdd.map(lambda x: x[0][0].strip().split())
             .filter(lambda x: len(x) == 3)
             .map(lambda x: (int(x[0]), int(x[1]), float(x[2])))
             .filter(lambda x: x[0] in region_node_ids_bc.value and x[1] in region_node_ids_bc.value)
)

edges_df = edges_filtered.toDF(["source", "destination", "weight"])

# Build RDD Graph for processing
edges_rdd = edges_df.rdd

# Build neighbors dictionary per node
neighbors_rdd = edges_rdd.flatMap(lambda x: [(x[0], x[1]), (x[1], x[0])]).groupByKey().mapValues(set).cache()
neighbors_dict = neighbors_rdd.collectAsMap()
neighbors_bc = sc.broadcast(neighbors_dict)

# Custom Betweenness Centrality using distributed BFS
def compute_partial_betweenness(start_node):
    from collections import deque, defaultdict

    neighbors = neighbors_bc.value
    stack = []
    predecessors = defaultdict(list)
    sigma = defaultdict(int)
    dist = defaultdict(lambda: -1)

    sigma[start_node] = 1
    dist[start_node] = 0
    queue = deque([start_node])

    while queue:
        v = queue.popleft()
        stack.append(v)
        for w in neighbors.get(v, []):
            if dist[w] < 0:
                dist[w] = dist[v] + 1
                queue.append(w)
            if dist[w] == dist[v] + 1:
                sigma[w] += sigma[v]
                predecessors[w].append(v)

    delta = defaultdict(float)
    while stack:
        w = stack.pop()
        for v in predecessors[w]:
            delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
        if w != start_node:
            yield (w, delta[w])

# Run parallel BC computation
bc_scores_rdd = sc.parallelize(region_node_ids).flatMap(compute_partial_betweenness)
bc_aggregated = bc_scores_rdd.reduceByKey(lambda a, b: a + b).mapValues(lambda x: x / 2.0)
bc_df = bc_aggregated.toDF(["nodeID", "Betweenness Centrality"])

# Join with coordinates
result_df = bc_df.join(nodes_df, on="nodeID")

# Convert to GeoJSON
features = (
    result_df.rdd.map(lambda row: geojson.Feature(
        geometry=geojson.Point((row["longitude"], row["latitude"])),
        properties={
            "NodeID": row["nodeID"],
            "Betweenness Centrality": row["Betweenness Centrality"]
        }
    )).collect()
)

feature_collection = geojson.FeatureCollection(features)

# Save to file
with open(output_geojson, "w") as f:
    geojson.dump(feature_collection, f)

print(f"GeoJSON saved to: {output_geojson}")
