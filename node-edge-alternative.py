from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, col, struct
from shapely.geometry import Point, LineString
import geojson

# Initialize Spark Session
spark = SparkSession.builder.appName("DistributedRoadGeoJSON").getOrCreate()

def create_nodes_and_edges_geojson_distributed(nodes_file, edges_distance_file, edges_travel_file, output_nodes_geojson, output_edges_geojson):
    # Read node coordinates (skip header)
    nodes_df = spark.read.text(nodes_file) \
        .rdd.zipWithIndex() \
        .filter(lambda x: x[1] > 0) \
        .map(lambda x: x[0].value.strip().split()) \
        .filter(lambda parts: len(parts) == 2) \
        .map(lambda parts: (float(parts[0]), float(parts[1]))) \
        .toDF(["latitude", "longitude"]) \
        .withColumn("nodeID", monotonically_increasing_id())

    # Read edges with distance
    edges_distance_df = spark.read.text(edges_distance_file) \
        .rdd.map(lambda x: x.value.strip().split()) \
        .filter(lambda parts: len(parts) == 3) \
        .map(lambda parts: (int(parts[0]), int(parts[1]), float(parts[2]))) \
        .toDF(["source", "destination", "distance"])

    # Read edges with travel time
    edges_travel_df = spark.read.text(edges_travel_file) \
        .rdd.map(lambda x: x.value.strip().split()) \
        .filter(lambda parts: len(parts) == 3) \
        .map(lambda parts: (int(parts[0]), int(parts[1]), float(parts[2]))) \
        .toDF(["source", "destination", "travel_time"])

    # Merge edge data
    edges_df = edges_distance_df.join(edges_travel_df, ["source", "destination"], "inner")

    # Collect nodes for mapping
    nodes_data = nodes_df.select("nodeID", "latitude", "longitude").rdd.map(lambda row: (row["nodeID"], (row["latitude"], row["longitude"]))).collectAsMap()

    # Create node GeoJSON features
    node_features = [
        geojson.Feature(
            geometry=Point((lon, lat)),
            properties={"nodeID": node_id}
        )
        for node_id, (lat, lon) in nodes_data.items()
    ]

    # Create edge GeoJSON features
    edge_features = []
    for row in edges_df.rdd.collect():
        if row.source in nodes_data and row.destination in nodes_data:
            source_coords = (nodes_data[row.source][1], nodes_data[row.source][0])
            dest_coords = (nodes_data[row.destination][1], nodes_data[row.destination][0])
            edge_features.append(
                geojson.Feature(
                    geometry=LineString([source_coords, dest_coords]),
                    properties={
                        "source": row.source,
                        "destination": row.destination,
                        "distance": row.distance,
                        "travel_time": row.travel_time
                    }
                )
            )

    # Write GeoJSON outputs
    with open(output_nodes_geojson, "w") as f:
        geojson.dump(geojson.FeatureCollection(node_features), f)
    with open(output_edges_geojson, "w") as f:
        geojson.dump(geojson.FeatureCollection(edge_features), f)

    print(f"Saved GeoJSON files:\n  Nodes -> {output_nodes_geojson}\n  Edges -> {output_edges_geojson}")

# Example file paths
create_nodes_and_edges_geojson_distributed(
    "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co",
    "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d",
    "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-t",
    "nodes.geojson",
    "edges.geojson"
)
