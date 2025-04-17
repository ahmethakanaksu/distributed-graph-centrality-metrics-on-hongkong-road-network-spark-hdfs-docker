from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from shapely.geometry import Point
import geojson

# Initialize Spark Session
spark = SparkSession.builder.appName("DistributedDegreeCentrality").getOrCreate()
sc = spark.sparkContext

def compute_degree(nodes_file, edges_file, output_geojson):
    # Define Smaller Region (Central Business District)
    region_lat_min, region_lat_max = 22.27, 22.29
    region_lon_min, region_lon_max = 114.15, 114.18

    # Read nodes
    nodes_rdd = spark.read.text(nodes_file).rdd.zipWithIndex().filter(lambda x: x[1] > 0)  # skip header
    parsed_nodes = (
        nodes_rdd.map(lambda x: (x[1] - 1, x[0][0].strip().split()))
                 .filter(lambda x: len(x[1]) == 2)
                 .map(lambda x: (int(x[0]), float(x[1][0]), float(x[1][1])))
    )
    nodes_df = parsed_nodes.toDF(["nodeID", "latitude", "longitude"])

    # Filter nodes within region
    region_nodes_df = nodes_df.filter(
        (col("latitude") >= region_lat_min) & (col("latitude") <= region_lat_max) &
        (col("longitude") >= region_lon_min) & (col("longitude") <= region_lon_max)
    )
    region_node_ids = [row["nodeID"] for row in region_nodes_df.collect()]
    region_node_ids_bc = sc.broadcast(set(region_node_ids))

    # Read and filter edges
    edges_rdd = spark.read.text(edges_file).rdd.zipWithIndex().filter(lambda x: x[1] > 0)  # skip header
    parsed_edges = (
        edges_rdd.map(lambda x: x[0][0].strip().split())
                 .filter(lambda x: len(x) == 3)
                 .map(lambda x: (int(x[0]), int(x[1]), float(x[2])))
                 .filter(lambda x: x[0] in region_node_ids_bc.value and x[1] in region_node_ids_bc.value)
    )
    edges_df = parsed_edges.toDF(["source", "destination", "distance"])

    # Create undirected edges (both directions)
    undirected_edges = edges_df.rdd.flatMap(lambda x: [(x["source"], 1), (x["destination"], 1)])

    # Count degrees (number of edges per node)
    degree_counts = undirected_edges.reduceByKey(lambda a, b: a + b)

    # Normalize degrees
    max_possible_degree = len(region_node_ids) - 1 if len(region_node_ids) > 1 else 1
    degree_centrality_rdd = degree_counts.mapValues(lambda degree: degree / max_possible_degree)

    # Convert to DataFrame
    degree_df = degree_centrality_rdd.toDF(["nodeID", "Degree Centrality"])

    # Join with node coordinates
    final_df = degree_df.join(region_nodes_df, on="nodeID", how="right").fillna(0)

    # Convert to GeoJSON
    features = (
        final_df.rdd.map(lambda row: geojson.Feature(
            geometry=geojson.Point((row["longitude"], row["latitude"])),
            properties={
                "NodeID": row["nodeID"],
                "Degree Centrality": row["Degree Centrality"]
            }
        )).collect()
    )

    feature_collection = geojson.FeatureCollection(features)

    # Save to file
    with open(output_geojson, "w") as f:
        geojson.dump(feature_collection, f)

    print(f"GeoJSON file saved as '{output_geojson}'")
    print(f"Processed {len(region_node_ids)} nodes for degree centrality.")

# File paths
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_distance_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d"
output_geojson = "degree_centrality.geojson"

# Execute
compute_degree(nodes_file, edges_distance_file, output_geojson)
