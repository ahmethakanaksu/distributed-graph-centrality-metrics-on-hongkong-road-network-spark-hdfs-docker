import pandas as pd
import networkx as nx
import geojson
from pyspark.sql import SparkSession
from shapely.geometry import Point, LineString
from collections import deque
import numpy as np
import geopandas as gpd
import community

# Initialize Spark Session
spark = SparkSession.builder.appName("RoadNetworkAnalysis").getOrCreate()
sc = spark.sparkContext

def compute_betweenness(nodes_file, edges_file, output_geojson):
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

    # Custom Betweenness Centrality Calculation
    def custom_betweenness_centrality(graph):
        betweenness = {node: 0.0 for node in graph.nodes()}
        nodes = list(graph.nodes())
        num_nodes = len(nodes)

        for i, source in enumerate(nodes):
            shortest_paths = {node: [] for node in nodes}
            shortest_paths[source] = [[source]]
            queue = [source]
            while queue:
                current = queue.pop(0)
                for neighbor in graph.neighbors(current):
                    if not shortest_paths[neighbor]:
                        queue.append(neighbor)
                        shortest_paths[neighbor] = [path + [neighbor] for path in shortest_paths[current]]
                    elif len(shortest_paths[neighbor][0]) == len(shortest_paths[current][0]) + 1:
                        shortest_paths[neighbor].extend([path + [neighbor] for path in shortest_paths[current]])
            
            dependency = {node: 0 for node in nodes}
            for target in reversed(nodes):
                if target != source:
                    for path in shortest_paths[target]:
                        for node in path[:-1]:
                            dependency[node] += 1 / len(shortest_paths[target])
                            betweenness[node] += dependency[node]
            
            print(f"Processed {i+1}/{num_nodes} nodes")
        return betweenness

    betweenness_centrality = custom_betweenness_centrality(G)

    # Convert betweenness centrality into a DataFrame
    betweenness_df = pd.DataFrame(list(betweenness_centrality.items()), columns=["nodeID", "Betweenness Centrality"])

    # Merge with node coordinates
    betweenness_df = betweenness_df.merge(region_nodes, on="nodeID")

    # Prepare GeoJSON data structure
    features = []
    for _, row in betweenness_df.iterrows():
        point = Point((row['longitude'], row['latitude']))
        feature = {
            "type": "Feature",
            "geometry": point.__geo_interface__,
            "properties": {
                "NodeID": row["nodeID"],
                "Betweenness Centrality": row["Betweenness Centrality"]
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
    print(f"Processed {len(region_nodes)} nodes for betweenness centrality.")

nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_distance_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d"
output_geojson = "betweenness_centrality.geojson"

# Compute Betweenness Centrality and Save
compute_betweenness(nodes_file, edges_distance_file, output_geojson)