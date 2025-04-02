import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from pyspark.sql import SparkSession
import logging

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("RoadNetworkAnalysis") \
    .getOrCreate()

# ============================
# Load Data from HDFS
# ============================
sc = spark.sparkContext
print(f"Total Cores Used: {sc.defaultParallelism}")

# File paths
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_distance_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d"
edges_travel_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-t"

# Read node coordinates (Skipping first line)
nodes_rdd = spark.read.text(nodes_file).rdd
nodes_rdd = nodes_rdd.zipWithIndex().filter(lambda x: x[1] > 0)  # Skip first line

nodes_list = []
for line, _ in nodes_rdd.collect():
    parts = line.value.strip().split()
    if len(parts) == 2:
        try:
            lat, lon = float(parts[0]), float(parts[1])
            nodes_list.append((lat, lon))
        except ValueError:
            print(f"Skipping invalid line: {line.value.strip()}")
nodes_rdd = sc.parallelize(nodes_list)
# Convert to DataFrame
nodes_df = pd.DataFrame(nodes_list, columns=["latitude", "longitude"])
nodes_df["nodeID"] = nodes_df.index

# Read edges (distance)
edges_distance_rdd = spark.read.text(edges_distance_file).rdd
edges_list = []
for line in edges_distance_rdd.collect():
    parts = line.value.strip().split()
    if len(parts) == 3:
        try:
            source, dest, distance = int(parts[0]), int(parts[1]), float(parts[2])
            edges_list.append((source, dest, distance))
        except ValueError:
            print(f"Skipping invalid line: {line.value.strip()}")
edges_rdd = sc.parallelize(edges_list)
edges_distance_df = pd.DataFrame(edges_list, columns=["source", "destination", "distance"])

# Read edges (travel time)
edges_travel_rdd = spark.read.text(edges_travel_file).rdd
edges_travel_list = []
for line in edges_travel_rdd.collect():
    parts = line.value.strip().split()
    if len(parts) == 3:
        try:
            source, dest, travel_time = int(parts[0]), int(parts[1]), float(parts[2])
            edges_travel_list.append((source, dest, travel_time))
        except ValueError:
            print(f"Skipping invalid line: {line.value.strip()}")
edges_travel_rdd = sc.parallelize(edges_travel_list)
edges_travel_df = pd.DataFrame(edges_travel_list, columns=["source", "destination", "travel_time"])

# Merge edge data
edges_df = pd.merge(edges_distance_df, edges_travel_df, on=["source", "destination"], how="inner")
print(edges_df.head())

# Convert nodes to GeoDataFrame
nodes_gdf = gpd.GeoDataFrame(
    nodes_df,
    geometry=gpd.points_from_xy(nodes_df.longitude, nodes_df.latitude),
    crs="EPSG:4326")

# Create GeoDataFrame for edges
def create_line_geometry(row):
    source_geom = nodes_gdf.loc[row["source"], "geometry"]
    dest_geom = nodes_gdf.loc[row["destination"], "geometry"]
    return LineString([source_geom, dest_geom])

edges_gdf = gpd.GeoDataFrame(edges_df, geometry=edges_df.apply(create_line_geometry, axis=1), crs="EPSG:4326")

# Build the NetworkX graph
G = nx.Graph()
for _, row in edges_df.iterrows():
    G.add_edge(row["source"], row["destination"], distance=row["distance"], travel_time=row["travel_time"])

# Visualize the network
fig, ax = plt.subplots(figsize=(12, 10))
nodes_gdf.plot(ax=ax, markersize=5, color="blue", label="Nodes")
edges_gdf.plot(ax=ax, linewidth=0.3, color="black", alpha=0.7, label="Edges")

plt.legend()
plt.title("Road Network Visualization (GIS)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
plt.savefig("/opt/road_network.png")  # Save inside the container

# Export nodes to GeoJSON
nodes_gdf.to_file("nodes.geojson", driver="GeoJSON")

# Export edges to GeoJSON
edges_gdf.to_file("edges.geojson", driver="GeoJSON")



import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from sklearn.cluster import KMeans

# Define real bounding boxes for the 5 neighborhoods
neighborhood_bounds = {
    "Central": [(22.276, 22.282), (114.154, 114.165)],
    "Victoria Peak": [(22.260, 22.270), (114.145, 114.155)],
    "Sai Wan": [(22.280, 22.287), (114.130, 114.148)],
    "Mid-Levels": [(22.275, 22.281), (114.148, 114.155)],
    "Wan Chai1": [(22.275, 22.280), (114.170, 114.180)],
}

# Function to filter nodes based on neighborhood boundaries
def assign_neighborhood(lat, lon):
    for neighborhood, ((lat_min, lat_max), (lon_min, lon_max)) in neighborhood_bounds.items():
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return neighborhood
    return "Outside"

# Apply filtering
nodes_gdf["neighborhood"] = nodes_gdf.apply(lambda row: assign_neighborhood(row["latitude"], row["longitude"]), axis=1)
filtered_nodes = nodes_gdf[nodes_gdf["neighborhood"] != "Outside"]

# Convert lat/lon to a NumPy array for clustering
node_coords = filtered_nodes[["latitude", "longitude"]].to_numpy()

# Apply KMeans clustering within this defined boundary
num_clusters = 5  # We want exactly 5 neighborhoods
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
filtered_nodes["cluster"] = kmeans.fit_predict(node_coords)

# Assign edges to clusters
edges_gdf["cluster"] = edges_gdf["source"].map(filtered_nodes.set_index("nodeID")["cluster"])

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(12, 8))

# Get unique clusters
unique_clusters = filtered_nodes["cluster"].unique()
num_clusters = len(unique_clusters)

# Use "tab10" colormap for distinct colors
cmap = matplotlib.colormaps["tab10"]
colors = [cmap(i / num_clusters) for i in range(num_clusters)]
cluster_colors = {cluster: colors[i] for i, cluster in enumerate(unique_clusters)}

# Plot nodes with different colors for each cluster
for cluster, color in cluster_colors.items():
    subset = filtered_nodes[filtered_nodes["cluster"] == cluster]
    subset.plot(ax=ax, color=color, markersize=5, label=f"Cluster {cluster}")

plt.legend(loc="upper right", fontsize="small", markerscale=2, title="Clusters")
plt.title("Segmented Neighborhoods in Hong Kong (Using KMeans)", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("hongkong_real_clusters.png", dpi=300, bbox_inches="tight")
plt.show()




import networkx as nx
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Convert filtered_nodes to Pandas for processing
filtered_nodes_df = filtered_nodes[["nodeID", "cluster"]]

# Step 1: Extract cluster subgraphs
cluster_graphs = {}
for cluster_id in filtered_nodes_df["cluster"].unique():
    cluster_nodes = filtered_nodes_df[filtered_nodes_df["cluster"] == cluster_id]["nodeID"].values
    subgraph = G.subgraph(cluster_nodes)  # Extract cluster-specific subgraph
    cluster_graphs[cluster_id] = subgraph

# Step 2: Compute Custom Closeness Centrality
custom_closeness = []
for cluster_id, subgraph in cluster_graphs.items():
    nodes = list(subgraph.nodes)
    for node in nodes:
        shortest_paths = nx.single_source_dijkstra_path_length(subgraph, node, weight="travel_time")  
        total_distance = sum(shortest_paths.values())  # Sum of shortest paths
        closeness_score = (len(nodes) - 1) / total_distance if total_distance > 0 else 0
        custom_closeness.append((node, cluster_id, closeness_score))

# Convert to DataFrame
closeness_df = pd.DataFrame(custom_closeness, columns=["nodeID", "cluster", "custom_closeness"])
print(closeness_df.head())

# Convert to Spark DataFrame
from pyspark.sql import Row

# Convert Pandas DataFrame to list of Rows for PySpark
closeness_rows = [Row(nodeID=int(row.nodeID), cluster=int(row.cluster), custom_closeness=float(row.custom_closeness)) for row in closeness_df.itertuples(index=False)]

# Create Spark DataFrame
spark_closeness_df = spark.createDataFrame(closeness_rows)



# Step 4: Visualization (Optional)
import matplotlib.pyplot as plt
import geopandas as gpd

filtered_nodes = filtered_nodes.merge(closeness_df, on="nodeID")

fig, ax = plt.subplots(figsize=(12, 8))
filtered_nodes.plot(ax=ax, column="custom_closeness", cmap="coolwarm", markersize=10, legend=True)
plt.title("Custom Closeness Centrality by Cluster")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("custom_closeness.png", dpi=300)
plt.show()

from sklearn.preprocessing import MinMaxScaler

# Ensure 'custom_closeness' exists
if "custom_closeness" in filtered_nodes.columns:
    scaler = MinMaxScaler(feature_range=(0, 1))  # Scale values between 0 and 1
    filtered_nodes["normalized_closeness"] = scaler.fit_transform(filtered_nodes[["custom_closeness"]])
else:
    print("Error: 'custom_closeness' column is missing in filtered_nodes!")


fig, ax = plt.subplots(figsize=(12, 8))

filtered_nodes.plot(
    ax=ax,
    column="normalized_closeness",
    cmap="viridis",  # Use a better color scale
    markersize=15,    # Increase size for visibility
    legend=True,
    vmin=0, vmax=1    # Stretch scale across full range
)

plt.title("Normalized Closeness Centrality by Cluster")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("custom_closeness_fixed.png", dpi=300)
plt.show()

import geopandas as gpd

# Ensure 'custom_closeness' exists before exporting
if "custom_closeness" in filtered_nodes.columns:
    # Create a GeoDataFrame with necessary columns
    closeness_gdf = filtered_nodes[["nodeID", "latitude", "longitude", "custom_closeness", "geometry"]]

    # Export to GeoJSON
    closeness_gdf.to_file("closeness_centrality.geojson", driver="GeoJSON")
    print("✅ GeoJSON file saved: closeness_centrality.geojson")
else:
    print("❌ Error: 'custom_closeness' column is missing in filtered_nodes!")
