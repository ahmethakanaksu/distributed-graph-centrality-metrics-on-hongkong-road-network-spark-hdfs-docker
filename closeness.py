import pandas as pd
import networkx as nx
import geojson
from pyspark.sql import SparkSession
from shapely.geometry import Point

# Initialize Spark Session
spark = SparkSession.builder.appName("RoadNetworkAnalysis").getOrCreate()
sc = spark.sparkContext

def compute_closeness(nodes_file, edges_file, output_geojson):
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

    # Custom Closeness Centrality Calculation
    def custom_closeness_centrality(graph):
        closeness = {}
        nodes = list(graph.nodes())
        num_nodes = len(nodes)

        # Calculate closeness centrality using NetworkX's built-in function
        for i, node in enumerate(nodes):
            lengths = nx.single_source_shortest_path_length(graph, node)
            total_distance = sum(lengths.values())
            
            # Only compute closeness for nodes that have finite distances
            if total_distance > 0 and total_distance != float('inf') * (num_nodes - 1):  # Avoid division by zero or disconnected
                closeness[node] = (num_nodes - 1) / total_distance
            else:
                closeness[node] = 0
            
            print(f"Processed {i+1}/{num_nodes} nodes")

        return closeness

    # Compute the closeness centrality for each node
    closeness_centrality = custom_closeness_centrality(G)

    # Add closeness centrality to the DataFrame using .loc to avoid the SettingWithCopyWarning
    region_nodes.loc[:, "Closeness Centrality"] = region_nodes["nodeID"].map(closeness_centrality)

    # Replace NaN values with 0 (or another default value of your choice)
    region_nodes.loc[:, "Closeness Centrality"].fillna(0, inplace=True)

    # Prepare GeoJSON data structure
    features = []
    for _, row in region_nodes.iterrows():
        point = Point((row['longitude'], row['latitude']))
        feature = {
            "type": "Feature",
            "geometry": point.__geo_interface__,
            "properties": {
                "NodeID": row["nodeID"],
                "Closeness Centrality": row["Closeness Centrality"]
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
    print(f"Processed {len(region_nodes)} nodes for closeness centrality.")

# File paths
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_distance_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d"
output_geojson = "closeness_centrality.geojson"

# Compute Closeness Centrality and Save
compute_closeness(nodes_file, edges_distance_file, output_geojson)
