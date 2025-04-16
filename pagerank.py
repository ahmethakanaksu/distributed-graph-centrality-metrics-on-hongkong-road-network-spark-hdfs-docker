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


def compute_pagerank(nodes_file, edges_file, output_file, 
                     region_lat_min=22.27, region_lat_max=22.29, 
                     region_lon_min=114.15, region_lon_max=114.18, 
                     alpha=0.85, max_iter=100, tol=1e-6):
    """Compute PageRank for nodes within the specified region and export to GeoJSON."""

    # Initialize Spark Session
    spark = SparkSession.builder.appName("PageRank").getOrCreate()
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
    G = nx.DiGraph()  # Directed graph for PageRank computation
    for _, row in edges_df.iterrows():
        G.add_edge(row["source"], row["destination"], weight=row["travel_time"])

    # Initialize PageRank
    pagerank = {node: 1.0 / len(G.nodes) for node in G.nodes}
    
    # PageRank Iteration (Power iteration method)
    for iteration in range(max_iter):
        new_pagerank = {}
        for node in G.nodes:
            rank_sum = 0
            for neighbor in G.predecessors(node):
                rank_sum += pagerank[neighbor] / len(list(G.neighbors(neighbor)))  # Normalize by the number of neighbors
            new_pagerank[node] = (1 - alpha) / len(G.nodes) + alpha * rank_sum
        
        # Convergence check
        diff = sum(abs(new_pagerank[node] - pagerank[node]) for node in G.nodes)
        pagerank = new_pagerank

        # Print progress
        if iteration % 10 == 0:
            print(f"Iteration {iteration}, Convergence Difference: {diff:.6f}")
        
        if diff < tol:
            print(f"Converged after {iteration} iterations.")
            break

    # Assign PageRank values to the nodes DataFrame
    nodes_df["PageRank"] = nodes_df["nodeID"].map(pagerank)

    # Create GeoDataFrame for Nodes
    nodes_gdf = gpd.GeoDataFrame(
        nodes_df,
        geometry=gpd.points_from_xy(nodes_df.longitude, nodes_df.latitude),
        crs="EPSG:4326"
    )

    # Export to GeoJSON
    nodes_gdf.to_file(output_file, driver="GeoJSON")
    print(f"PageRank values saved to: {output_file}")

# File paths
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_travel_time_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-t"
output_geojson = "pagerank_centrality.geojson"
    
compute_pagerank(
   nodes_file,edges_travel_time_file, output_geojson
)

