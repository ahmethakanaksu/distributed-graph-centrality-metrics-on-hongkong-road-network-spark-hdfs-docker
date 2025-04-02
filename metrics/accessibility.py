import pandas as pd
import networkx as nx
import geojson
from pyspark.sql import SparkSession
from shapely.geometry import Point, LineString
from collections import deque
import numpy as np
import geopandas as gpd

# Initialize Spark Session
spark = SparkSession.builder.appName("RoadNetworkAnalysis").getOrCreate()
sc = spark.sparkContext


def compute_accessibility(nodes_file, edges_file, output_file, 
                                           region_lat_min=22.27, region_lat_max=22.29, 
                                           region_lon_min=114.15, region_lon_max=114.18):
    """Compute the Accessibility Index for nodes in the popular region and export to GeoJSON."""
    
    # Initialize Spark Session
    spark = SparkSession.builder.appName("AccessibilityAnalysis").getOrCreate()
    sc = spark.sparkContext

    # Load Nodes Data
    nodes_rdd = spark.read.text(nodes_file).rdd
    nodes_rdd = nodes_rdd.zipWithIndex().filter(lambda x: x[1] > 0)  # Skip first line

    nodes_list = []
    for i, (line, _) in enumerate(nodes_rdd.collect()):
        parts = line.value.strip().split()
        if len(parts) == 2:
            try:
                lat, lon = float(parts[0]), float(parts[1])
                if region_lat_min <= lat <= region_lat_max and region_lon_min <= lon <= region_lon_max:
                    nodes_list.append((i, lat, lon))
            except ValueError:
                print(f"Skipping invalid line: {line.value.strip()}")

    # Create DataFrame for Nodes
    nodes_df = pd.DataFrame(nodes_list, columns=["nodeID", "latitude", "longitude"])

    # Load Edges Data
    edges_rdd = spark.read.text(edges_file).rdd
    edges_list = []

    for line in edges_rdd.collect():
        parts = line.value.strip().split()
        if len(parts) == 3:
            try:
                source, dest, travel_time = int(parts[0]), int(parts[1]), float(parts[2])
                if travel_time > 0:  # Avoid division by zero
                    edges_list.append((source, dest, travel_time))
            except ValueError:
                print(f"Skipping invalid line: {line.value.strip()}")

    # Create DataFrame for Edges
    edges_df = pd.DataFrame(edges_list, columns=["source", "destination", "travel_time"])

    # Build the NetworkX Graph
    G = nx.Graph()
    for _, row in edges_df.iterrows():
        G.add_edge(row["source"], row["destination"], weight=row["travel_time"])

    # Compute Accessibility Index for each node
    accessibility_scores = {}
    total_nodes = len(nodes_df)
    for idx, node in enumerate(nodes_df["nodeID"]):
        total_score = 0
        try:
            # Get shortest paths from the node to others using travel time as weight
            shortest_paths = nx.single_source_dijkstra_path_length(G, node, weight="weight")
            for _, travel_time in shortest_paths.items():
                total_score += 1 / travel_time if travel_time > 0 else 0  # Avoid division by zero
            accessibility_scores[node] = total_score
        except nx.NetworkXNoPath:
            accessibility_scores[node] = 0  # No connectivity

        # Print the number of processed nodes
        if (idx + 1) % 100 == 0:  # Print progress every 100 nodes
            print(f"Processed {idx + 1} out of {total_nodes} nodes.")

    # Map Accessibility Index scores to nodes DataFrame
    nodes_df["Accessibility Index"] = nodes_df["nodeID"].map(accessibility_scores)

    # Convert to GeoDataFrame
    nodes_gdf = gpd.GeoDataFrame(
        nodes_df,
        geometry=gpd.points_from_xy(nodes_df.longitude, nodes_df.latitude),
        crs="EPSG:4326"
    )

    # Export to GeoJSON
    nodes_gdf.to_file(output_file, driver="GeoJSON")
    print(f"Saved: {output_file}")


# File paths
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_travel_time_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-t"
output_geojson = "accessibility_centrality.geojson"
    
compute_accessibility(
   nodes_file,edges_travel_time_file, output_geojson
)