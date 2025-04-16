import pandas as pd
import networkx as nx
import geojson
from pyspark.sql import SparkSession
from shapely.geometry import Point

# Initialize Spark Session
spark = SparkSession.builder.appName("RoadNetworkAnalysis").getOrCreate()
sc = spark.sparkContext

def compute_degree(nodes_file, edges_file, output_geojson):
    # Read node coordinates
    nodes_rdd = spark.read.text(nodes_file).rdd
    nodes_rdd = nodes_rdd.zipWithIndex().filter(lambda x: x[1] > 0)  # Skip first line

    nodes_list = [
        (float(parts[0]), float(parts[1]))
        for line, _ in nodes_rdd.collect()
        if (parts := line.value.strip().split()) and len(parts) == 2 and not line.value.startswith("#")
    ]
    nodes_df = pd.DataFrame(nodes_list, columns=["latitude", "longitude"])
    nodes_df["nodeID"] = nodes_df.index

    # Read edges (distance)
    edges_distance_rdd = spark.read.text(edges_file).rdd
    edges_list = [
        (int(parts[0]), int(parts[1]), float(parts[2]))
        for line in edges_distance_rdd.collect()
        if (parts := line.value.strip().split()) and len(parts) == 3 and not line.value.startswith("#")
    ]
    edges_distance_df = pd.DataFrame(edges_list, columns=["source", "destination", "distance"])

    # Define Smaller Region (Central Business District)
    region_lat_min, region_lat_max = 22.27, 22.29
    region_lon_min, region_lon_max = 114.15, 114.18

    # Filter nodes based on the defined region
    region_nodes = nodes_df[
        (nodes_df['latitude'] >= region_lat_min) & (nodes_df['latitude'] <= region_lat_max) & 
        (nodes_df['longitude'] >= region_lon_min) & (nodes_df['longitude'] <= region_lon_max)
    ]
    region_node_ids = set(region_nodes['nodeID'].values)

    # Filter edges to include only those within the region
    filtered_edges = edges_distance_df[
        (edges_distance_df['source'].isin(region_node_ids)) & (edges_distance_df['destination'].isin(region_node_ids))
    ]

    # Create NetworkX Graph
    G = nx.Graph()
    for _, row in filtered_edges.iterrows():
        G.add_edge(row["source"], row["destination"], weight=row["distance"])

    # Custom Degree Centrality Calculation
    def custom_degree_centrality(graph):
        degree_centrality = {}
        nodes = list(graph.nodes())
        max_possible_degree = len(nodes) - 1

        # Calculate degree centrality
        for i, node in enumerate(nodes):
            degree = graph.degree(node)
            degree_centrality[node] = degree / max_possible_degree
            print(f"Processed {i+1}/{len(nodes)} nodes")

        return degree_centrality

    # Compute the degree centrality for each node
    degree_centrality = custom_degree_centrality(G)

    # Add degree centrality to the DataFrame using .loc to avoid the SettingWithCopyWarning
    region_nodes.loc[:, "Degree Centrality"] = region_nodes["nodeID"].map(degree_centrality)

    # Replace NaN values with 0 (or another default value of your choice)
    region_nodes.loc[:, "Degree Centrality"].fillna(0, inplace=True)

    # Prepare GeoJSON data structure
    features = []
    for _, row in region_nodes.iterrows():
        point = Point((row['longitude'], row['latitude']))
        feature = {
            "type": "Feature",
            "geometry": point.__geo_interface__,
            "properties": {
                "NodeID": row["nodeID"],
                "Degree Centrality": row["Degree Centrality"]
            }
        }
        features.append(feature)

    # Create GeoJSON
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # Save to a GeoJSON file
    with open(output_geojson, "w") as f:
        geojson.dump(geojson_data, f)

    print(f"GeoJSON file saved as '{output_geojson}'")

    # Print how many nodes were processed
    print(f"Processed {len(region_nodes)} nodes for degree centrality.")

# File paths
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_distance_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d"
output_geojson = "degree_centrality.geojson"

# Compute Degree Centrality and Save
compute_degree(nodes_file, edges_distance_file, output_geojson)
