from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType, IntegerType, StructType, StructField
import geopandas as gpd
from shapely.geometry import Point

def compute_pagerank_limited(
    nodes_file, edges_file, output_file,
    region_lat_min=22.27, region_lat_max=22.29,
    region_lon_min=114.15, region_lon_max=114.18,
    alpha=0.85, max_iter=100, tol=1e-6):

    # Start Spark Session
    spark = SparkSession.builder.appName("DistributedPageRank50Nodes").getOrCreate()
    sc = spark.sparkContext

    # ---------------------
    # Load and Filter Nodes
    # ---------------------
    raw_nodes_rdd = spark.read.text(nodes_file).rdd.zipWithIndex().filter(lambda x: x[1] > 0)

    def parse_node(x):
        index = x[1] - 1
        try:
            parts = list(map(float, x[0][0].strip().split()))
            if len(parts) != 2:
                return None
            return (index, parts[0], parts[1])  # (nodeID, lat, lon)
        except:
            return None

    nodes_parsed = raw_nodes_rdd.map(parse_node).filter(lambda x: x is not None)

    nodes_filtered = nodes_parsed.filter(
        lambda x: region_lat_min <= x[1] <= region_lat_max and region_lon_min <= x[2] <= region_lon_max
    )

    # Only take the first 50
    limited_nodes = nodes_filtered.zipWithIndex().filter(lambda x: x[1] < 50).map(lambda x: x[0]).cache()

    node_ids = limited_nodes.map(lambda x: x[0]).collect()
    node_id_set = set(node_ids)
    broadcast_node_ids = sc.broadcast(node_id_set)

    node_schema = StructType([
        StructField("nodeID", IntegerType(), False),
        StructField("latitude", FloatType(), False),
        StructField("longitude", FloatType(), False)
    ])
    nodes_df = spark.createDataFrame(limited_nodes, schema=node_schema)

    # ---------------------
    # Load and Filter Edges
    # ---------------------
    raw_edges_rdd = spark.read.text(edges_file).rdd.map(lambda row: row[0].strip().split())

    def parse_edge(parts):
        try:
            if len(parts) != 3:
                return None
            source = int(parts[0])
            target = int(parts[1])
            weight = float(parts[2])
            if weight <= 0:
                return None
            return (source, target)
        except:
            return None

    edges = raw_edges_rdd.map(parse_edge).filter(lambda x: x is not None)
    filtered_edges = edges.filter(
        lambda x: x[0] in broadcast_node_ids.value and x[1] in broadcast_node_ids.value
    )

    # ---------------------
    # Build Adjacency List
    # ---------------------
    links = filtered_edges.groupByKey().cache()
    nodes = links.keys().distinct().cache()
    N = nodes.count()
    ranks = nodes.map(lambda node: (node, 1.0 / N))

    # ---------------------
    # PageRank Iteration
    # ---------------------
    for iteration in range(max_iter):
        contribs = links.join(ranks).flatMap(
            lambda x: [(dest, x[1][1] / len(x[1][0])) for dest in x[1][0]]
        )
        new_ranks = contribs.reduceByKey(lambda x, y: x + y).mapValues(
            lambda rank: (1 - alpha) / N + alpha * rank
        )
        diff = ranks.join(new_ranks).mapValues(lambda x: abs(x[0] - x[1])).values().sum()
        ranks = new_ranks

        if iteration % 10 == 0:
            print(f"Iteration {iteration}, diff: {diff:.6f}")
        if diff < tol:
            print(f"Converged after {iteration} iterations.")
            break

    # ---------------------
    # Join with Coordinates
    # ---------------------
    ranks_df = ranks.toDF(["nodeID", "PageRank"])
    result_df = nodes_df.join(ranks_df, on="nodeID")

    # ---------------------
    # Write GeoJSON with Logging Every 10 Nodes
    # ---------------------
    pandas_df = result_df.toPandas()
    features = []
    for i, row in pandas_df.iterrows():
        if i % 10 == 0:
            print(f"Processed {i} nodes...")

        point = Point(row["longitude"], row["latitude"])
        features.append({
            "nodeID": row["nodeID"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "PageRank": row["PageRank"],
            "geometry": point
        })

    gdf = gpd.GeoDataFrame(features, geometry="geometry", crs="EPSG:4326")
    gdf.to_file(output_file, driver="GeoJSON")
    print(f"PageRank results saved to {output_file}")

# ---------------------
# Run the Function
# ---------------------
nodes_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.co"
edges_file = "hdfs://spark-yarn-master:8080/data/Hongkong/Hongkong.road-t"
output_geojson = "pagerank_50nodes.geojson"

compute_pagerank_limited(nodes_file, edges_file, output_geojson)
