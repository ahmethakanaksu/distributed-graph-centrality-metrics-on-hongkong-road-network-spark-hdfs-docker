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


def create_nodes_and_edges_geojson(nodes_file, edges_distance_file, edges_travel_file, output_nodes_geojson, output_edges_geojson):
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

    # Export nodes to GeoJSON
    nodes_gdf.to_file(output_nodes_geojson, driver="GeoJSON")
    print(f"Node GeoJSON file saved as '{output_nodes_geojson}'")

    # Export edges to GeoJSON
    edges_gdf.to_file(output_edges_geojson, driver="GeoJSON")
    print(f"Edge GeoJSON file saved as '{output_edges_geojson}'")

    # File paths for output GeoJSON files
output_nodes_geojson = "nodes.geojson"
output_edges_geojson = "edges.geojson"
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_distance_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-d"
edges_travel_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-t"

create_nodes_and_edges_geojson(nodes_file,edges_distance_file,edges_travel_file, output_nodes_geojson,output_edges_geojson)