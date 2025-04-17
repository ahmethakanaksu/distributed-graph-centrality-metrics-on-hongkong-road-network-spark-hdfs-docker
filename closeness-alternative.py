from pyspark.sql import SparkSession
from shapely.geometry import Point
import geojson
import networkx as nx
import os

# Initialize Spark session
spark = SparkSession.builder.appName("DistributedClosenessCentrality").getOrCreate()
sc = spark.sparkContext

def compute_closeness_distributed(nodes_file, edges_file, output_geojson,
                                   region_lat_min=22.27, region_lat_max=22.29,
                                   region_lon_min=114.15, region_lon_max=114.18,
                                   max_nodes=50):
    # Load and parse node file
    nodes_rdd = spark.read.text(nodes_file).rdd.zipWithIndex().filter(lambda x: x[1] > 0)
    
    def parse_node(line_index):
        line, idx = line_index
        parts = line.value.strip().split()
        if len(parts) == 2 and not line.value.startswith("#"):
            try:
                lat, lon = float(parts[0]), float(parts[1])
                return [(idx, lat, lon)] if (region_lat_min <= lat <= region_lat_max and region_lon_min <= lon <= region_lon_max) else []
            except:
                return []
        return []

    filtered_nodes = nodes_rdd.flatMap(parse_node).zipWithIndex().map(lambda x: (x[1], x[0]))  # (newID, (oldID, lat, lon))
    region_nodes_dict = filtered_nodes.collectAsMap()  # Needed for referencing filtered node IDs

    # Broadcast node set for edge filtering
    filtered_node_ids = set(x[1][0] for x in region_nodes_dict.items())
    broadcast_node_ids = sc.broadcast(filtered_node_ids)

    # Load and parse edge file
    edges_rdd = spark.read.text(edges_file).rdd.filter(lambda x: not x.value.startswith("#"))

    def parse_edge(line):
        parts = line.value.strip().split()
        if len(parts) == 3:
            try:
                src, dst, dist = int(parts[0]), int(parts[1]), float(parts[2])
                if src in broadcast_node_ids.value and dst in broadcast_node_ids.value:
                    return [(src, dst, dist)]
            except:
                return []
        return []

    filtered_edges = edges_rdd.flatMap(parse_edge)
    edge_list = filtered_edges.collect()

    # Create NetworkX graph
    G = nx.Graph()
    for src, dst, dist in edge_list:
        G.add_edge(src, dst, weight=dist)

    # Closeness centrality
    closeness_scores = {}
    nodes_to_process = list(filtered_node_ids)[:max_nodes]

    for i, node in enumerate(nodes_to_process):
        lengths = nx.single_source_dijkstra_path_length(G, node)
        total_distance = sum(lengths.values())

        if total_distance > 0:
            closeness_scores[node] = (len(lengths) - 1) / total_distance
        else:
            closeness_scores[node] = 0.0

        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{len(nodes_to_process)} nodes")

    # Write GeoJSON
    features = []
    for new_id, (old_id, lat, lon) in region_nodes_dict.items():
        if old_id in closeness_scores:
            point = Point((lon, lat))
            features.append(geojson.Feature(geometry=point, properties={
                "NodeID": int(old_id),
                "Closeness Centrality": closeness_scores[old_id]
            }))

    geojson_obj = geojson.FeatureCollection(features)

    with open(output_geojson, "w") as f:
        geojson.dump(geojson_obj, f)

    print(f"Saved {len(features)} nodes to {output_geojson}")

# Run it
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d"
output_geojson = "closeness_centrality.geojson"

compute_closeness_distributed(nodes_file, edges_file, output_geojson)
