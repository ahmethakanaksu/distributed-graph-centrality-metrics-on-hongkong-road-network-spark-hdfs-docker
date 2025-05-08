[Distributed Graph Centrality Metrics on Hong Kong Island region Dataset
using Apache Spark]{.c8 .c25 .c44}

[]{.c3}

[Course]{.c12}[: Big Data (BIL401)]{.c6}

[]{.c6}

[Team Members]{.c12}[: ]{.c6}

[Ahmet Hakan Aksu]{.c6}

[Başak Güney]{.c6}

[]{.c6}

[Date]{.c12}[: 17/04/2025]{.c6}

[]{.c3}

[]{.c3}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

[]{.c8 .c12}

1.  [ Abstract]{.c8 .c15}

[]{.c3}

[Understanding the structural importance of intersections and roads in a
transportation network is crucial for optimizing traffic flow, urban
planning, and infrastructure resilience. This project focuses on
computing graph centrality metrics for a large-scale road network using
distributed graph processing techniques in Apache Spark. Unlike
traditional approaches that rely on built-in GraphFrames functions, we
aim to adapt these centrality measures to distributed data to enhance
flexibility and efficiency.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[The dataset used is the Central Hong Kong Island region within the
coordinates: region_lat_min=22.27, region_lat_max=22.29,
region_lon_min=114.15, region_lon_max=114.18, consisting of 7,564 nodes
(intersections) and 16,426 edges (roads), with attributes such as
geographical coordinates, road distances, and estimated travel times. We
implement five key centrality metrics: Degree Centrality, Closeness
Centrality, Betweenness Centrality, PageRank, and Accessibility. Each
metric is designed to leverage the distributed computing capabilities of
Apache Spark, ensuring scalability for large-scale networks.]{.c8 .c4
.c9}

[]{.c8 .c4 .c9}

[By computing these centrality metrics, we aim to identify highly
connected intersections, key transit hubs, and critical roads affecting
traffic flow. The insights gained can be applied in smart transportation
planning, traffic congestion mitigation, and urban analytics.]{.c8 .c4
.c9}

[]{.c8 .c4 .c9}

[This research contributes to the fields of big data graph processing,
distributed computing, and transportation network analysis,
demonstrating the practical applications of large-scale graph analytics
in urban development.]{.c8 .c4 .c9}

[]{.c3}

[]{.c3}

[]{.c3}

[]{.c8 .c15}

[]{.c8 .c15}

[]{.c8 .c15}

[]{.c8 .c15}

[]{.c8 .c15}

2.  [ Introduction]{.c8 .c15}

[]{.c3}

[Problem Statement:]{.c25 .c38}

[The ability to identify crucial intersections and roads in urban
transportation networks is essential for traffic optimization, urban
planning, and developing resilient infrastructure. ]{.c3}

[]{.c3}

[The main question guiding this research is: How can we utilize graph
centrality metrics to improve urban transportation systems, including
transit hub placement, emergency evacuation routes, and congestion
reduction, within a densely populated region?]{.c3}

[]{.c3}

[Objectives:]{.c38 .c10 .c41}

[The objectives of this project are:]{.c3}

[]{.c3}

[To implement custom distributed algorithms for calculating graph
centrality metrics on the Central Hong Kong Island region within the
coordinates: region_lat_min=22.27, region_lat_max=22.29,
region_lon_min=114.15, region_lon_max=114.18 dataset using Apache
Spark.]{.c3}

[]{.c3}

[To enhance efficiency and scalability by leveraging distributed
computing capabilities.]{.c3}

[]{.c3}

[To provide insights into the structural importance of intersections and
roads, aiding in smart city planning and traffic flow
optimization.]{.c3}

[]{.c3}

[]{.c3}

[]{.c3}

[Scope:]{.c38 .c25}

[This project involves the analysis of the Central Hong Kong Island
region within the coordinates: region_lat_min=22.27,
region_lat_max=22.29, region_lon_min=114.15, region_lon_max=114.18
dataset, consisting of 7,564 nodes and 16,426 edges. We focus on
implementing five key centrality metrics using Apache Spark\'s
distributed computing framework: Degree Centrality, Closeness
Centrality, Betweenness Centrality, PageRank, and Accessibility. The
dataset is processed using Spark RDD transformations, with custom
algorithms developed to enhance flexibility and efficiency.]{.c3}

[]{.c3}

[]{.c3}

[]{.c3}

[]{.c8 .c19}

[ ]{.c8 .c9 .c11}

[]{.c8 .c19}

[]{.c3}

### []{.c8 .c19} {#h.oz14e8wl27o1 .c5 .c24}

3.  ### [ Data Review: Hong Kong Island Road Network]{.c8 .c15} {#h.tbb0cp7sjiry style="display:inline"}

The dataset used for the analysis represents the entire road network of
Hong Kong Island, with a focus on the Central Hong Kong Island[ region.
The full dataset consists of:]{.c3}

- [Total Nodes:]{.c25}[ 43,620 nodes (intersections)\
  ]{.c3}
- [Total Edges:]{.c25}[ 91,542 edges (roads)\
  ]{.c3}

The dataset includes data on the nodes (intersections) and edges (roads)
along with their associated attributes such as geographical coordinates,
road distances, and estimated travel times. The Central Hong Kong Island
region[ is a subset of the larger dataset, focusing on a smaller,
defined area of interest.]{.c3}

[]{.c3}

[Central Hong Kong Island Region Focus]{.c8 .c10}

The subset of the dataset used for specific analysis represents
the Central Hong Kong Island [region within the following
coordinates:]{.c3}

- [Latitude:]{.c25}[ 22.27 ≤ latitude ≤ 22.29\
  ]{.c3}
- [Longitude:]{.c25}[ 114.15 ≤ longitude ≤ 114.18\
  ]{.c3}

[This region consists of:]{.c3}

- [Nodes:]{.c25}[ 7,564 intersections (nodes)\
  ]{.c3}
- [Edges:]{.c25}[ 16,426 roads (edges)\
  ]{.c3}

This smaller region allows for a more focused analysis and makes the
data manageable for computation and visualizations related to [city
planning, traffic flow analysis, route optimization, and accessibility
studies.]{.c3}

[The dataset is divided into three primary files, each containing
specific information about the road network:]{.c3}

1.  [hongkong.co]{.c39 .c25}[ (Nodes File)\
    ]{.c8 .c10}

- [Description:]{.c25}[ Contains the coordinates of each intersection
  (node) in the road network.\
  ]{.c3}
- [Example Content:]{.c8 .c10}

                     
 [![](images/image27.png){style="width: 624.00px; height: 329.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 329.33px;"}

[]{.c3}

[hongkong.road-d]{.c25 .c39}[ (Edge File with Distances)]{.c8 .c10}

- [Description:]{.c25}[ Contains the distances between connected nodes
  (intersections).\
  ]{.c3}
- [Example Content:]{.c8 .c10}

[![](images/image41.png){style="width: 624.00px; height: 293.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 293.33px;"}

[]{.c3}

[hongkong.road-t]{.c39 .c25}[ (Edge File with Travel Times)]{.c8 .c10}

- [Description:]{.c25}[ Contains the estimated travel times for roads
  between connected nodes.\
  ]{.c3}
- [Example Content:]{.c8 .c10}

[![](images/image33.png){style="width: 624.00px; height: 270.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 270.67px;"}

[]{.c3}

You can access data from
[[https://yzengal.github.io/datasets/](https://www.google.com/url?q=https://yzengal.github.io/datasets/&sa=D&source=editors&ust=1746730804775467&usg=AOvVaw2vp26I0wRNUDWutEfSCqU8){.c37}]{.c29}[.]{.c3}

[]{.c3}

### []{.c8 .c19} {#h.ka8dkxwp0ofw .c5 .c24}

### [4) Environment Setup ]{.c8 .c15} {#h.g1gv9ic7m5ea .c5}

[The environment setup for this project involves configuring an Apache
Spark cluster with a master node, multiple worker nodes, and a Spark
History Server. The setup ensures that you can scale your processing by
adjusting the number of worker nodes and manage the processing history
through the History Server. The data and metric implementation files are
handled within Docker, and additional configurations are made for
loading data into HDFS.]{.c3}

[Below is the detailed environment setup process:]{.c3}

### [Dockerfile Analysis for Distributed Spark-Hadoop Setup]{.c8 .c1} {#h.37q8hjtj7nq8 .c5}

[This Dockerfile outlines the environment setup for a distributed Spark
and Hadoop system, designed to run on top of a Docker container. Below
is a step-by-step analysis, explaining each section and its role within
the larger context of the distributed system.]{.c3}

[1. Base Image Setup:]{.c8 .c10}

[![](images/image34.png){style="width: 624.00px; height: 81.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 81.33px;"}

- [Base Image]{.c25}: The image starts from python:3.10-bullseye[, which
  is an official Python image based on Debian Bullseye. This is chosen
  because Python is necessary for running PySpark and related scripts.\
  ]{.c3}
- [Spark & Hadoop Versions]{.c25}: Two build arguments are defined
  (SPARK_VERSION and HADOOP_VERSION[), which will be used to download
  specific versions of Spark and Hadoop.]{.c3}

[]{.c3}

[2. Installing System Dependencies:]{.c8 .c10}

[![](images/image60.png){style="width: 624.00px; height: 222.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 222.67px;"}\
[Update & Install Dependencies]{.c25}: Updates the package lists for the
apt[ package manager and installs essential packages, including:\
]{.c3}

- [System Tools]{.c25}: sudo, curl, vim, unzip, rsync[ for general
  system operations.\
  ]{.c3}
- [Java]{.c25}: openjdk-11-jdk[ for running Spark and Hadoop, as both
  rely on Java for operation.\
  ]{.c3}
- [Development Tools]{.c25}: build-essential,
  software-properties-common[ for building software and managing
  repositories.\
  ]{.c3}
- [SSH]{.c25}[: Required for remote communication between nodes in the
  Spark cluster.\
  ]{.c3}

[Clean-up]{.c25}[: After the installation, the package cache is cleaned
to reduce the image size, which is a best practice for Docker
images.]{.c3}

[]{.c3}

[]{.c3}

[3. Setup Directories for Spark and Hadoop:]{.c8 .c10}

[]{.c8 .c10}

[![](images/image50.png){style="width: 624.00px; height: 113.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 113.33px;"}

[]{.c3}

[Environment Variables]{.c25}: [SPARK_HOME]{.c9 .c22} and
[HADOOP_HOME]{.c9 .c22} are set to default locations ([/opt/spark]{.c9
.c22} and [/opt/hadoop]{.c9 .c22}[) unless already set.\
]{.c3}

[Directory Creation]{.c25}: Ensures that the directories for Spark and
Hadoop are created. The [WORKDIR]{.c9 .c22}[ command sets the working
directory to Spark's home.]{.c3}

[]{.c3}

[]{.c3}

[4. Download and Install Spark:]{.c8 .c10}

[]{.c8 .c10}

[![](images/image24.png){style="width: 654.48px; height: 66.40px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 654.48px; height: 66.40px;"}

- [Download Spark: ]{.c25}Downloads Spark from Apache's archives using
  [curl]{.c9 .c22}. The version is specified by the [SPARK_VERSION]{.c9
  .c22}[ argument.\
  ]{.c3}
- [Extract and Cleanup: ]{.c25}The [tar]{.c9 .c22} command extracts
  Spark into the Spark directory ([/opt/spark]{.c9 .c22}[), stripping
  the leading components of the archive to avoid creating an unnecessary
  folder. The downloaded archive is removed to save space.\
  ]{.c3}

[5. Download and Install Hadoop:]{.c8 .c10}

[]{.c8 .c10}

[![](images/image2.png){style="width: 624.00px; height: 56.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 56.00px;"}

- [Download Hadoop:]{.c25} Similar to Spark, Hadoop is downloaded from
  Apache's website and extracted to the specified directory
  [/opt/hadoop]{.c9 .c22}.[\
  ]{.c8 .c10}
- [Extract and Cleanup: ]{.c25}[Hadoop is extracted and the archive is
  deleted after installation.\
  ]{.c3}

[6. Python Dependencies Setup:]{.c8 .c10}

[![](images/image32.png){style="width: 624.00px; height: 84.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 84.00px;"}

[]{.c8 .c10}

[Switch to ]{.c25}[pyspark]{.c25}[ Base: ]{.c25}The image is now
extended from the [spark-base]{.c9 .c22}[ to install PySpark-specific
Python dependencies.\
]{.c3}

[Install Python Packages: ]{.c25}The requirements.txt file (which
presumably contains necessary Python packages) is copied into the
container, and pip3[ installs the dependencies.]{.c3}

[]{.c3}

[]{.c3}

[7. Set Environment Variables:]{.c8 .c10}

[]{.c8 .c10}

[![](images/image28.png){style="width: 624.00px; height: 304.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 304.00px;"}

[JAVA_HOME: ]{.c25}Sets the JAVA_HOME[ environment variable to the Java
11 installation.\
]{.c3}

[PATH Updates: ]{.c25}The paths for Spark, Hadoop, and Java binaries are
added to the PATH[ environment variable so that commands for Spark,
Hadoop, and Java can be executed easily.\
]{.c3}

[Spark Master Configuration: ]{.c25}Sets the Spark master URL
(SPARK_MASTER), which is the address of the Spark cluster, and
SPARK_MASTER_HOST[ for the host configuration.\
]{.c3}

[Python Configuration: ]{.c25}The PYSPARK_PYTHON[ variable is set to use
Python 3.\
]{.c3}

[Hadoop Configuration Directory: ]{.c25}HADOOP_CONF_DIR[ is set to point
to the Hadoop configuration directory.\
]{.c3}

[Library Path: ]{.c25}Updates the LD_LIBRARY_PATH[ to include Hadoop\'s
native libraries.]{.c3}

[]{.c3}

### [8. HDFS and YARN User Setup:]{.c8 .c10} {#h.si8ede66hfvr .c5}

[]{.c3}

[![](images/image47.png){style="width: 624.00px; height: 96.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 96.00px;"}

- [User Setup]{.c25}: Sets Hadoop's user environment variables for
  different components (e.g., NameNode, DataNode, ResourceManager).
  Here, the users are set to [root]{.c9 .c22}[, which is not recommended
  for production but may be used for simplicity in a development setup.\
  ]{.c3}

[9. Add Configuration Files:]{.c8 .c10}

[]{.c3}

[![](images/image42.png){style="width: 624.00px; height: 85.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 85.33px;"}

- [Hadoop Configuration]{.c25}: Adds JAVA_HOME to Hadoop's environment
  configuration file (hadoop-env.sh[).\
  ]{.c3}
- [Copy Configuration Files]{.c25}: Copies custom Spark and Hadoop
  configuration files (e.g., spark-defaults.conf, core-site.xml,
  hdfs-site.xml[, etc.) into the respective directories.]{.c3}

[]{.c3}

[10. Permissions and SSH Setup:]{.c8 .c10}

[]{.c8 .c10}

[![](images/image40.png){style="width: 624.00px; height: 193.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 193.33px;"}

[]{.c8 .c10}

[Make Spark Scripts Executable: ]{.c25}Grants execution permissions to
Spark scripts located in the sbin and bin[ directories.\
]{.c3}

[SSH Setup: ]{.c25}[Generates SSH keys and sets up passwordless SSH for
cluster communication. This is useful for distributed operations in
Spark/Hadoop clusters.]{.c3}

[]{.c8 .c10}

[11. Data and Metrics Files Setup:]{.c8 .c10}

[]{.c8 .c10}

[![](images/image57.png){style="width: 624.00px; height: 129.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 129.33px;"}

- [Copy Data Files: ]{.c25}The road network data files (Hongkong.co,
  Hongkong.road-d, and Hongkong.road-t[) are copied into the container.
  These files contain the nodes and edges for the road network
  analysis.\
  ]{.c3}
- [Permissions:]{.c25}[ The files are given full permissions to ensure
  they can be read and written to by Spark and other processes.\
  ]{.c3}

### [12. Entrypoint Script Setup:]{.c8 .c10} {#h.up6ht9e368pr .c5}

[]{.c3}

[![](images/image3.png){style="width: 624.00px; height: 164.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 164.00px;"}

- [Entrypoint]{.c25}: The entrypoint.sh[ script is copied into the
  container, and it\'s responsible for starting the necessary services
  (e.g., Spark, Hadoop) when the container runs.\
  ]{.c3}
- [Expose SSH:]{.c25}[ Port 22 (used for SSH) is exposed to allow for
  external communication.\
  ]{.c3}
- [Windows Line Ending Fix:]{.c25} The sed command is used to convert
  Windows-style line endings (CRLF) to Unix-style (LF) in the
  entrypoint.sh[ script.\
  ]{.c3}

[]{.c3}

### [Detailed Step-by-Step Explanation of ]{.c1 .c42}[entrypoint-yarn.sh]{.c8 .c1} {#h.38c2yg47j541 .c5}

The entrypoint-yarn.sh script is responsible for configuring and
launching different components of a Spark cluster running on YARN. It
determines the role of the container (master, worker, or history[) and
executes the necessary services.]{.c3}

## [Step 1: Capturing the Workload Type]{.c8 .c10} {#h.rswhreq216yf .c32}

[![](images/image22.png){style="width: 399.50px; height: 104.59px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 399.50px; height: 104.59px;"}

- [#!/bin/bash :]{.c25}[ This tells the system that the script should be
  executed using the Bash shell.\
  ]{.c3}
- [SPARK_WORKLOAD=\$1]{.c25} [:]{.c25}The first argument passed to the
  script (\$1) is assigned to the variable SPARK_WORKLOAD[.\
  ]{.c3}

<!-- -->

- If executed as ./entrypoint-yarn.sh master, then
  SPARK_WORKLOAD=\"master\"[.\
  ]{.c3}
- If executed as ./entrypoint-yarn.sh worker, then
  SPARK_WORKLOAD=\"worker\"[.\
  ]{.c3}
- If executed as ./entrypoint-yarn.sh history, then
  SPARK_WORKLOAD=\"history\"[.\
  ]{.c3}

<!-- -->

- [echo \"SPARK_WORKLOAD: \$SPARK_WORKLOAD\" ]{.c25}[:]{.c25}[ Prints
  the role of the node to help with debugging.\
  ]{.c3}

[Step 2: Start the SSH Service]{.c8 .c10}

[![](images/image36.png){style="width: 524.50px; height: 44.55px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 524.50px; height: 44.55px;"}

- [Starts the SSH service]{.c25}[ inside the container.\
  ]{.c3}
- [Why is this necessary?\
  ]{.c8 .c10}

<!-- -->

- [Hadoop and Spark use passwordless SSH for communication between nodes
  in the cluster.\
  ]{.c3}
- [Without this, worker nodes wouldn't be able to connect to the master,
  and distributed computations wouldn't work.\
  ]{.c3}

## [Step 3: Master Node Setup]{.c8 .c10} {#h.q0rinsfmbnb9 .c32}

[![](images/image16.png){style="width: 511.50px; height: 42.63px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 511.50px; height: 42.63px;"}

- If the container is supposed to act as a Spark master, then the script
  executes the following steps.

[3.1 Format the HDFS Namenode]{.c8 .c10}

[![](images/image49.png){style="width: 624.00px; height: 26.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 26.67px;"}

- [Formats the Namenode, which manages the metadata of the Hadoop
  Distributed File System (HDFS).\
  ]{.c3}
- [The -nonInteractive flag ensures that the process does not ask for
  confirmation (to avoid manual intervention).]{.c3}

### [3.2 Start Essential Hadoop and YARN Services]{.c8 .c10} {#h.h19frvc7tu3q .c5}

[![](images/image54.png){style="width: 541.50px; height: 87.65px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 541.50px; height: 87.65px;"}

- [Starts Hadoop Namenode:]{.c25}[ Manages file system metadata and
  handles data distribution.\
  ]{.c3}
- [Starts Secondary Namenode:]{.c25}[ Periodically takes snapshots of
  the Namenode metadata (to avoid excessive memory usage).\
  ]{.c3}
- [Starts YARN ResourceManager:]{.c25} Manages cluster resources and job
  scheduling for Spark tasks.\

[3.3 Create Required Directories in HDFS]{.c8 .c10}

- Creates the /spark-logs[ directory in HDFS (used for logging Spark
  applications).\
  ]{.c3}
- The while[ loop keeps trying until the directory is successfully
  created.\
  ]{.c3}
- [Why is this needed?]{.c3}

<!-- -->

- The Spark History Server depends on log files stored in
  /spark-logs[.]{.c3}
- [If the directory is missing, the History Server cannot track past
  jobs.]{.c3}

[![](images/image14.png){style="width: 539.50px; height: 106.34px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 539.50px; height: 106.34px;"}

- Creates a directory for Spark data (/opt/spark/data[).\
  ]{.c3}
- Creates a directory for the Hong Kong road network dataset
  (/data/Hongkong[).\
  ]{.c3}
- These directories help organize the dataset within HDFS.[\
  ]{.c8 .c10}

[3.4 Upload Dataset to HDFS]{.c8 .c10}

[![](images/image46.png){style="width: 624.00px; height: 72.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 72.00px;"}

- The -put -f[ command copies the dataset files into HDFS.\
  ]{.c3}
- [-f]{.c39} (force) ensures that if the file already exists, it is
  replaced.[\
  ]{.c8 .c10}

[![](images/image19.png){style="width: 624.00px; height: 41.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 41.33px;"}

- Copies any local files in /opt/spark/data/[ to HDFS.\
  ]{.c3}
- Lists the files in HDFS (hdfs dfs -ls) to verify successful upload.[\
  ]{.c8 .c10}

[Step 4: Worker Node Setup]{.c25}

[![](images/image7.png){style="width: 567.50px; height: 54.57px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 567.50px; height: 54.57px;"}

- [Starts HDFS DataNode:]{.c25}[ Stores actual data blocks for
  distributed storage.\
  ]{.c3}
- [Starts YARN NodeManager:]{.c25} Manages computing resources and
  executes Spark tasks.\

[Step 5: Spark History Server Setup]{.c8 .c10}

[![](images/image17.png){style="width: 575.50px; height: 52.57px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 575.50px; height: 52.57px;"}

- [If the container should act as the Spark History Server, it follows
  these steps.]{.c3}

[]{.c3}

[5.1 Wait for ]{.c25}[/spark-logs]{.c25}[ Directory]{.c8 .c10}

[]{.c8 .c10}

[![](images/image1.png){style="width: 624.00px; height: 133.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 133.33px;"}

- Checks whether the /spark-logs[ directory exists in HDFS.\
  ]{.c3}
- hdfs dfs -test -d[ checks if a directory exists.\
  ]{.c3}
- If it does not exist, it waits (sleep 1[) and retries.\
  ]{.c3}
- [This ensures that the logs directory is created before starting the
  History Server.]{.c3}

[]{.c8 .c10}

[5.2 Start Spark History Server]{.c8 .c10}

[]{.c8 .c10}

[![](images/image11.png){style="width: 629.50px; height: 45.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 629.50px; height: 45.00px;"}

- [Starts the Spark History Server, which allows users to view past job
  executions via a web interface.]{.c3}

[]{.c3}

[Step 6: Keep Container Running]{.c8 .c10}

[]{.c8 .c10}

[![](images/image59.png){style="width: 453.50px; height: 37.08px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 453.50px; height: 37.08px;"}

- [This prevents the container from exiting immediately after executing
  the script.\
  ]{.c3}
- [Why is this needed?\
  ]{.c3}

<!-- -->

- [When running in Docker, a container stops if its main process
  terminates.\
  ]{.c3}
- tail -f /dev/null keeps the process alive indefinitely.

[]{.c8 .c10}

## [Key Takeaways]{.c8 .c10} {#h.fqqxvyeum7up .c32}

1.  Modular and flexible. The script supports different roles
    ([master]{.c9 .c22}, [worker]{.c9 .c22}, [history]{.c9 .c22}[).\
    ]{.c3}
2.  [Ensures necessary directories exist before launching services.\
    ]{.c3}
3.  [Automates HDFS setup and Spark cluster initialization.\
    ]{.c3}
4.  [Uses loops and retries to prevent failures due to missing
    directories.\
    ]{.c3}
5.  [Keeps the container alive to maintain cluster operations.]{.c3}

[]{.c8 .c10}

[]{.c8 .c10}

[]{.c8 .c10}

[]{.c8 .c10}

[]{.c8 .c10}

[]{.c8 .c10}

[]{.c8 .c10}

[]{.c8 .c10}

[]{.c8 .c10}

[]{.c8 .c10}

### []{.c8 .c1} {#h.syu06qjdwhsv .c5 .c24}

### [Docker Compose Analysis for Distributed Spark-Hadoop Setup]{.c8 .c1} {#h.fs3hwtabg298 .c5}

## [1. Service Descriptions]{.c8 .c10} {#h.1io997he1be9 .c32}

### [1.1 Spark-YARN Master]{.c8 .c10} {#h.8qp6j067jvl2 .c5}

The spark-yarn-master[ service acts as the primary control node,
managing Spark and HDFS operations.]{.c3}

#### [Configuration:]{.c8 .c10} {#h.xh2486oofc12 .c23}

[![](images/image10.png){style="width: 529.50px; height: 357.24px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 529.50px; height: 357.24px;"}

[]{.c3}

#### [Explanation:]{.c8 .c10} {#h.8okzma6n2e9w .c23}

- [Container Name:]{.c25} da-spark-yarn-master[ ensures consistent
  referencing.]{.c3}
- [Build:]{.c25} Uses the specified Dockerfile[ to create the
  image.]{.c3}
- [Image:]{.c25} Named da-spark-yarn-image[ to maintain consistency
  across services.]{.c3}
- [Entry Point:]{.c25} Runs entrypoint.sh with the \"master\"[ argument,
  initiating:]{.c3}

<!-- -->

- [HDFS NameNode]{.c3}
- [HDFS Secondary NameNode]{.c3}
- [YARN ResourceManager]{.c3}
- [Spark master node]{.c3}

<!-- -->

- [Volumes:]{.c25}[ Mounts local directories for data and Spark
  applications.]{.c3}
- [Environment Variables:]{.c25} Loaded from [.env.spark]{.c9
  .c22}[.]{.c3}
- [Ports:]{.c8 .c10}

<!-- -->

- [8080]{.c9 .c22} (Spark Web UI, mapped to [9090]{.c9
  .c22}[ externally)]{.c3}
- [9870]{.c9 .c22}[ (HDFS NameNode UI)]{.c3}
- [7077]{.c9 .c22}[ (Spark master node)]{.c3}
- [8088]{.c9 .c22}[ (YARN ResourceManager UI)]{.c3}

### [1.2 Spark-YARN Worker]{.c8 .c10} {#h.fhjuq0y2uiwc .c5}

The spark-yarn-worker[ service adds computational capacity by running
DataNodes and NodeManagers.]{.c3}

#### [Configuration:]{.c8 .c10} {#h.d0ey83wfxgpb .c23}

[![](images/image35.png){style="width: 521.50px; height: 246.68px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 521.50px; height: 246.68px;"}

#### [Explanation:]{.c8 .c10} {#h.3thkwb3yiwde .c23}

- [Image:]{.c25} Uses the same da-spark-yarn-image[ to ensure
  uniformity.]{.c3}
- [Entry Point:]{.c25} Runs entrypoint.sh with \"worker\"[,
  initiating:]{.c3}

<!-- -->

- [HDFS DataNode]{.c3}
- [YARN NodeManager]{.c3}

<!-- -->

- [Dependencies:]{.c25} Ensures spark-yarn-master[ starts before
  workers.]{.c3}
- [Environment Variables & Volumes:]{.c25}[ Same as the master
  node.]{.c3}

### []{.c8 .c10} {#h.d5k1m7dbnalj .c5 .c24}

### []{.c8 .c10} {#h.duby3dbkra13 .c5 .c24}

### []{.c8 .c10} {#h.5j46j7xx6g0j .c5 .c24}

### []{.c8 .c10} {#h.ct6b9n2gszr3 .c5 .c24}

### []{.c8 .c10} {#h.isigni1if95j .c5 .c24}

### [2.3 YARN History Server]{.c8 .c10} {#h.g6bl99afrbfi .c5}

The yarn-history-server[ tracks completed Spark jobs.]{.c3}

#### [Configuration:]{.c8 .c10} {#h.ei2s7n1cbtpz .c23}

[![](images/image48.png){style="width: 475.01px; height: 234.50px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 475.01px; height: 234.50px;"}

[]{.c3}

#### [Explanation:]{.c8 .c10} {#h.nv0s7y3hudnr .c23}

- [Container Name:]{.c25} da-spark-yarn-history[ for
  identification.]{.c3}
- [Image:]{.c25} Uses da-spark-yarn-image[ for consistency.]{.c3}
- [Entry Point:]{.c25} Runs entrypoint.sh with \"history\"[ to start the
  history server.]{.c3}
- [Dependencies:]{.c25} Waits for spark-yarn-master[ to initialize
  first.]{.c3}
- [Port Mapping:]{.c25} Exposes history server UI on [18080]{.c9
  .c22}[.]{.c3}

### [Running the Docker Compose Setup with Scaling]{.c8 .c10} {#h.ptv5s8sb1yr3 .c5}

To scale the number of worker nodes in your Spark-YARN cluster, you can
use the \--scale flag with Docker Compose. This command allows you to
define how many instances of the spark-yarn-worker[ service you want to
run.]{.c3}

#### [Step 1: Scale the Worker Nodes]{.c8 .c10} {#h.cqqkh55uuyy .c23}

[To scale the worker nodes, use the following command:]{.c3}

[![](images/image8.png){style="width: 624.00px; height: 45.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 45.33px;"}

[Explanation]{.c25}[:]{.c3}

- \--scale spark-yarn-worker=3: This flag instructs Docker Compose to
  create 3 instances of the spark-yarn-worker service. These worker
  nodes will connect to the master node (spark-yarn-master[) to form a
  distributed Spark cluster.\
  ]{.c3}
- This command will create 3 worker containers, each running a Spark
  worker node, while the master node (spark-yarn-master) and history
  server (yarn-history-server[) will be initialized as per the
  configuration.]{.c3}

[Connecting Running Containers with VSCODE]{.c8 .c1}

### [Step 1: Install the \"Dev Containers\" Extension]{.c8 .c10} {#h.dx0rrpwb2129 .c5}

1.  [Open VSCode.\
    ]{.c3}
2.  Go to the Extensions view by clicking the Extensions icon on the
    left sidebar (or press Ctrl+Shift+X[).\
    ]{.c3}
3.  [In the search bar, type Dev Containers.\
    ]{.c3}
4.  [Install the Dev Containers extension by Microsoft.]{.c3}

[![](images/image31.png){style="width: 624.00px; height: 94.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 94.67px;"}

[]{.c8 .c1}

### [Step 2: Open VSCode Command Palette]{.c8 .c10} {#h.pvh6qk40yzwj .c5}

[To interact with Docker containers, you\'ll need to open the Command
Palette in VSCode:]{.c3}

1.  Press Ctrl+Shift+P (or F1) to open the Command Palette.

### [Step 3: Attach to a Running Container]{.c8 .c10} {#h.d0zwu1v41cz7 .c5}

1.  [Type Dev Containers: Attach to Running Container\... in the Command
    Palette.\
    ]{.c3}
2.  [Select the running container you want to connect to. You should see
    a list of containers running on your system.\
    ]{.c3}
3.  Click on the container you want to attach to (e.g.,
    da-spark-yarn-master or da-spark-yarn-worker-1[).]{.c3}

[![](images/image52.png){style="width: 624.00px; height: 366.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 366.67px;"}

[![](images/image29.png){style="width: 624.00px; height: 193.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 193.33px;"}

[![](images/image55.png){style="width: 624.00px; height: 350.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 350.67px;"}

[Spark Web UI]{.c8 .c1}

[\
]{.c25}[![](images/image38.png){style="width: 624.00px; height: 122.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 122.67px;"}

[![](images/image23.png){style="width: 624.00px; height: 269.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 269.33px;"}

[![](images/image51.png){style="width: 624.00px; height: 285.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 285.33px;"}

[![](images/image15.png){style="width: 624.00px; height: 294.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 294.67px;"}

[]{.c8 .c1}

[]{.c8 .c1}

[]{.c8 .c1}

[]{.c8 .c1}

[]{.c8 .c1}

[]{.c8 .c1}

[Hadoop Web UI]{.c8 .c1}

[![](images/image30.png){style="width: 624.00px; height: 285.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 285.33px;"}

[]{.c8 .c1}

[![](images/image13.png){style="width: 624.00px; height: 452.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 452.00px;"}

[]{.c3}

[5) Centrality Metric Implementations]{.c8 .c15}

[]{.c8 .c4 .c9}

### [5.1 Accessibility Centrality]{.c8 .c19} {#h.rez6uegdsygz .c5}

[Accessibility Centrality quantifies how reachable a node is within a
network based on travel cost --- in this case, ]{.c11}[travel
time]{.c7}[ between intersections. Unlike Closeness Centrality, which
averages distances from one node to all others, Accessibility focuses on
]{.c11}[how many nodes can reach a given node quickly]{.c7}[, regardless
of path length.]{.c8 .c9 .c11}

[The ]{.c11}[mathematical formulation]{.c7}[ for Accessibility of a node
is:]{.c8 .c9 .c11}

[![](images/image56.png){style="width: 187.00px; height: 72.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 187.00px; height: 72.00px;"}

[Where:]{.c8 .c9 .c11}

- [A(v): Accessibility score of node v\
  ]{.c8 .c9 .c11}
- [R(v): Set of nodes reachable from v\
  ]{.c8 .c9 .c11}
- [d(u,v): Shortest path travel time from node u to node v\
  ]{.c8 .c9 .c11}

[This sum of ]{.c11}[inverse travel times]{.c7}[ means that shorter
paths contribute more to the accessibility score, and distant or
unreachable nodes contribute less or nothing. As such, nodes with high
accessibility are those that can be reached ]{.c11}[quickly]{.c7}[ and
from ]{.c11}[many locations]{.c7}[.]{.c8 .c9 .c11}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

#### [Implementation Steps]{.c8 .c21} {#h.78r08u55fzg7 .c23}

[The computation was implemented by integrating ]{.c11}[Apache
Spark]{.c7}[ for distributed data processing and ]{.c11}[graph
analytics]{.c7}[ for path computation. The steps are as follows:]{.c8
.c9 .c11}

[]{.c8 .c4 .c9}

#### [5.1.1. Data Loading from HDFS using Spark RDDs]{.c8 .c1} {#h.tg6clovv1xdo .c23}

- [Both ]{.c11}[node]{.c7}[ and ]{.c11}[edge]{.c7}[ data files were
  stored on ]{.c11}[Hadoop Distributed File System (HDFS)]{.c7}[ to
  allow distributed access across the Spark cluster.\
  ]{.c8 .c9 .c11}
- [The files were read using Spark and converted into ]{.c11}[RDDs
  (Resilient Distributed Datasets)]{.c7}[ to enable ]{.c11}[parallel
  filtering, parsing, and transformation]{.c7}[ operations.\
  ]{.c8 .c9 .c11}
- [This step ensures scalable data preprocessing, which is essential for
  large urban networks.\
  ]{.c8 .c9 .c11}

#### [5.1.2. Spatial Filtering of Relevant Nodes]{.c8 .c1} {#h.tl2u5ddpar6i .c23}

- [Only nodes within a predefined bounding box were retained, focusing
  the analysis on the ]{.c11}[Central Hong Kong Island]{.c7}[ area.\
  ]{.c8 .c9 .c11}
- [This spatial filter reduced unnecessary computation outside the
  region of interest and improved performance.\
  ]{.c8 .c9 .c11}

[]{.c8 .c4 .c9}

#### [5.1.3. Edge Preparation with Travel Time Weights]{.c8 .c1} {#h.4utpvka0jt53 .c23}

- [Edges (road segments) were extracted with their corresponding
  ]{.c11}[source node, destination node, and travel
  time]{.c7}[ attributes.\
  ]{.c8 .c9 .c11}
- [Invalid entries and non-positive travel times were discarded to
  maintain the integrity of the weight calculations.\
  ]{.c8 .c9 .c11}
- [These edges were used to construct the ]{.c11}[weighted graph]{.c7}[,
  where ]{.c11}[travel time]{.c7}[ was treated as the cost function for
  each edge.\
  ]{.c8 .c9 .c11}

#### [5.1.4. Graph Construction and Accessibility Computation]{.c1 .c8} {#h.1qyitml1ff0g .c23}

- [A graph was constructed from the filtered data. Each node represents
  an intersection, and each edge represents a road segment weighted by
  travel time.\
  ]{.c8 .c9 .c11}
- [For each node, ]{.c11}[shortest path travel times]{.c7}[ to all
  reachable nodes were computed using ]{.c11}[Dijkstra's
  algorithm]{.c7}[, with ]{.c11}[travel time as the weight]{.c7}[.\
  ]{.c8 .c9 .c11}
- [The ]{.c11}[Accessibility score]{.c7}[ was then computed as the sum
  of ]{.c11}[1/travel time]{.c7}[ for all reachable nodes.\
  ]{.c8 .c9 .c11}
- [This favors nodes that are reachable via many ]{.c11}[short and
  fast]{.c7}[ paths.\
  ]{.c8 .c9 .c11}

[]{.c8 .c4 .c9}

#### [5.1.5. Output Generation for Visualization]{.c8 .c1} {#h.h1opxfaxgnn0 .c23}

- [Each node's Accessibility score was added to its spatial data.\
  ]{.c8 .c9 .c11}
- [The final dataset was converted to a ]{.c11}[GeoDataFrame]{.c7}[ and
  exported as a ]{.c11}[GeoJSON]{.c7}[ file.\
  ]{.c8 .c9 .c11}
- [This format allowed for easy visualization and analysis in geospatial
  platforms like ]{.c11}[QGIS]{.c7}[, where nodes could be colored based
  on accessibility levels.\
  ]{.c8 .c9 .c11}

[]{.c8 .c4 .c9}

### []{.c8 .c19} {#h.aahn51odlc85 .c5 .c24}

### [5.2 Betweenness Centrality]{.c8 .c19} {#h.pdll5cdv8qy5 .c5}

[Betweenness Centrality]{.c7}[ quantifies how often a node appears on
the shortest paths between all pairs of nodes in a network. It
highlights nodes that serve as ]{.c11}[critical bridges or transfer
points]{.c7}[, making it especially useful for identifying intersections
likely to experience congestion or failure impact.]{.c8 .c9 .c11}

[The mathematical formulation of Betweenness Centrality for a node
is:]{.c8 .c9 .c11}

[![](images/image43.png){style="width: 199.00px; height: 73.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 199.00px; height: 73.00px;"}

[Where:]{.c8 .c9 .c11}

- [σst​: Total number of shortest paths between nodes s and t\
  ]{.c8 .c9 .c11}
- [σst(v): Number of those paths that pass through node v\
  ]{.c8 .c9 .c11}

[A higher value of CB(v) indicates that the node plays a more central
role in connecting different parts of the network.]{.c8 .c9 .c11}

#### []{.c8 .c1} {#h.aaer0y1pi201 .c23 .c31}

#### [Implementation Steps]{.c21 .c42} {#h.qhvkmzbf5irp .c23}

[To calculate this metric efficiently over a real-world transportation
network, the computation combined ]{.c11}[distributed data preprocessing
via Apache Spark]{.c7}[ with a ]{.c11}[custom path-counting algorithm
implemented]{.c7}[. Here\'s how the process was structured:]{.c8 .c9
.c11}

#### []{.c8 .c10} {#h.diggtu3bcqrk .c23 .c31}

#### [5.2.1. Distributed Data Loading from HDFS using Spark RDDs]{.c8 .c1} {#h.7bnej9h9btig .c23}

- [Node and edge datasets were stored on ]{.c11}[Hadoop Distributed File
  System (HDFS)]{.c7}[.\
  ]{.c8 .c9 .c11}
- [Spark was used to read these files into ]{.c11}[Resilient Distributed
  Datasets (RDDs)]{.c7}[, enabling parallel preprocessing of node
  coordinates and edge attributes.\
  ]{.c8 .c9 .c11}
- [This allowed scalable filtering, parsing, and preparation of large
  road network data.\
  ]{.c8 .c9 .c11}

#### [5.2.2. Spatial Filtering to Central Region]{.c8 .c1} {#h.5gk3iop08bf0 .c23}

- [To narrow the analysis to the ]{.c11}[Central Hong Kong
  Island]{.c7}[ area, a bounding box filter was applied.\
  ]{.c8 .c9 .c11}
- [Only nodes falling within the latitude and longitude range of the
  target region were included.\
  ]{.c8 .c9 .c11}
- [Subsequently, edges were filtered to include only those
  ]{.c11}[connecting nodes within the same region]{.c7}[, ensuring the
  graph remained local and contextually relevant.\
  ]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.2.3. Graph Construction with Weighted Edges]{.c8 .c1} {#h.3f636rfbruhb .c23}

- [A graph was constructed using the filtered node and edge data.\
  ]{.c8 .c9 .c11}
- [Each edge represented a road segment and was weighted by
  ]{.c11}[distance]{.c7}[, which served as the cost function during
  shortest path calculations.\
  ]{.c8 .c9 .c11}
- [The resulting graph captured the regional structure of the road
  network for detailed centrality analysis.\
  ]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.2.4. Custom Betweenness Centrality Algorithm]{.c8 .c1} {#h.8ta0fzbmuoo6 .c23}

- [Instead of relying on built-in functions, a ]{.c11}[custom
  algorithm]{.c7}[ was implemented to compute betweenness centrality
  explicitly.\
  ]{.c8 .c9 .c11}
- [For each source node, all shortest paths to other nodes were
  generated using ]{.c11}[breadth-first search]{.c7}[ (BFS)-based
  traversal.\
  ]{.c8 .c9 .c11}
- [Every time a node appeared in a shortest path between two others, its
  centrality score was incremented proportionally.\
  ]{.c8 .c9 .c11}
- [This method counted ]{.c11}[all equally shortest paths]{.c7}[,
  distributing importance across multiple routes, ensuring accuracy in
  the presence of multiple equivalent paths.\
  ]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.2.5. GeoJSON Output for Geospatial Visualization]{.c8 .c1} {#h.uw5hunf0tcr3 .c23}

- [The computed centrality values were merged with node coordinates.\
  ]{.c8 .c9 .c11}
- [The final results were exported in ]{.c11}[GeoJSON format]{.c7}[,
  making them ready for visualization in GIS software like
  ]{.c11}[QGIS]{.c7}[.\
  ]{.c8 .c9 .c11}
- [This enabled effective mapping of critical intersections and visual
  identification of high-betweenness nodes.]{.c8 .c9 .c11}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

### [5.3 Closeness Centrality]{.c8 .c19} {#h.k4o1msm0g08g .c5}

[Closeness Centrality]{.c7}[ measures how close a node is to all other
nodes in a network. A node with high Closeness Centrality can reach the
rest of the network with ]{.c11}[shorter average paths]{.c7}[, making it
a strong candidate for emergency service placement, commercial hubs, or
administrative centers.]{.c8 .c9 .c11}

[The formal definition is:]{.c8 .c9 .c11}

[![](images/image6.png){style="width: 243.00px; height: 75.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 243.00px; height: 75.00px;"}

[Where:]{.c8 .c9 .c11}

- [Cc(v) is the closeness centrality of node v\
  ]{.c8 .c9 .c11}
- [N is the total number of nodes in the graph\
  ]{.c8 .c9 .c11}
- [d(v,u) is the length (distance) of the shortest path between nodes v
  and u\
  ]{.c8 .c9 .c11}

[Nodes with higher closeness values are those that can reach other parts
of the network more efficiently. This metric provides a global
perspective on a node's position within the overall structure.]{.c8 .c9
.c11}

#### []{.c8 .c7} {#h.9g8ghodpex77 .c23 .c31}

#### [Implementation Steps]{.c8 .c21} {#h.kpvg1au8zm5n .c23}

[To compute Closeness Centrality on a real-world road network, the
system uses a combination of ]{.c11}[Apache Spark]{.c7}[ for distributed
preprocessing and graph-based computations. The process unfolds as
follows:]{.c8 .c9 .c11}

#### []{.c8 .c7} {#h.bj1f3fcetsgp .c23 .c31}

#### [5.3.1. Distributed Data Loading from HDFS using Spark RDDs]{.c8 .c1} {#h.vjpje7k16s0a .c23}

- [Node and edge data were stored in the ]{.c11}[Hadoop Distributed File
  System (HDFS)]{.c7}[ and accessed using ]{.c11}[Spark]{.c7}[.\
  ]{.c8 .c9 .c11}
- [The files were read into ]{.c11}[RDDs (Resilient Distributed
  Datasets)]{.c7}[ for scalable, parallel parsing and filtering of raw
  data entries.\
  ]{.c8 .c9 .c11}
- [This distributed setup ensures efficient preprocessing even with
  thousands of geographic records.\
  ]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.3.2. Regional Filtering of Nodes and Edges]{.c8 .c1} {#h.c4q6dsyzsn54 .c23}

- [To focus the analysis on a specific region, a ]{.c11}[bounding box
  filter]{.c7}[ was applied to include only the nodes located within
  ]{.c11}[Central Hong Kong Island]{.c7}[.\
  ]{.c8 .c9 .c11}
- [Edges were then filtered to retain only those that connect nodes
  within this regional subset, ensuring relevance to the local analysis
  area.\
  ]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.3.3. Graph Construction with Weighted Edges]{.c8 .c1} {#h.thd5gocwvx5q .c23}

- [A ]{.c11}[weighted undirected graph]{.c7}[ was created from the
  filtered data, where nodes represent intersections and edges represent
  road segments with ]{.c11}[distance]{.c7}[ as weight.\
  ]{.c8 .c9 .c11}
- [This graph forms the structure on which centrality computations are
  performed.\
  ]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.3.4. Closeness Centrality Computation]{.c8 .c1} {#h.f048jkuimsrs .c23}

- [For each node in the graph, the ]{.c11}[shortest path
  lengths]{.c7}[ to all other reachable nodes were calculated.\
  ]{.c8 .c9 .c11}
- [The closeness value was computed as the ]{.c11}[inverse of the total
  distance]{.c7}[ to all other nodes, scaled by the total number of
  nodes.\
  ]{.c8 .c9 .c11}
- [If a node was disconnected or unreachable from others, its closeness
  value was set to zero to reflect its isolation in the network.\
  ]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.3.5. GeoJSON Output for Visualization]{.c8 .c1} {#h.7lx68w1lew6g .c23}

- [The resulting Closeness Centrality values were merged with each
  node's geographic coordinates.\
  ]{.c8 .c9 .c11}
- [The enriched data was exported as a ]{.c11}[GeoJSON]{.c7}[ file,
  enabling intuitive visualization of central and peripheral locations
  in GIS platforms such as ]{.c11}[QGIS]{.c7}[.]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

### [5.4 Degree Centrality]{.c8 .c19} {#h.azv5ohppnxl4 .c5}

[Degree Centrality]{.c25}[ measures how many direct connections (edges)
a node has to other nodes. In transportation networks, it reflects how
many roads or paths are connected to a specific intersection. High
degree values indicate ]{.c11}[highly connected]{.c7}[, while low values
point to more isolated.]{.c8 .c9 .c11}

[The formal definition of Degree Centrality for a node v is:]{.c8 .c9
.c11}

[![](images/image25.png){style="width: 180.00px; height: 67.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 180.00px; height: 67.00px;"}

[Where:]{.c8 .c9 .c11}

- [CD(v): Degree centrality of node v\
  ]{.c8 .c9 .c11}
- [deg(v): Number of direct connections (edges) node v has\
  ]{.c8 .c9 .c11}
- [N: Total number of nodes in the network\
  ]{.c8 .c9 .c11}

[This normalization ensures that the centrality values fall within the
range \[0,1\], making them comparable across networks of different
sizes.]{.c8 .c9 .c11}

#### []{.c8 .c1} {#h.9kbg55r6i36o .c23 .c31}

#### [Implementation Steps]{.c1 .c42} {#h.9vj07axrzh63 .c23}

[The metric was computed by combining ]{.c11}[distributed data
preprocessing using Apache Spark]{.c7}[ with ]{.c11}[graph-based
analysis using NetworkX]{.c7}[. Below is the breakdown of the
implementation:]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.4.1. Distributed Data Loading from HDFS using Spark RDDs]{.c8 .c1} {#h.c97a1q4uxzm .c23}

- [The node and edge data were stored in the ]{.c11}[Hadoop Distributed
  File System (HDFS)]{.c7}[ and read using ]{.c11}[Apache Spark]{.c7}[.\
  ]{.c8 .c9 .c11}
- [Spark loaded these files into ]{.c11}[Resilient Distributed Datasets
  (RDDs)]{.c7}[, enabling efficient and parallel parsing of geographic
  and structural data.\
  ]{.c8 .c9 .c11}

#### [5.4.2. Geographic Filtering to Central Region]{.c8 .c1} {#h.ebm4sajqb97 .c23}

- [Nodes were filtered to include only those falling within a
  ]{.c11}[bounding box representing the Central Hong Kong
  Island]{.c7}[ area.\
  ]{.c8 .c9 .c11}
- [Edges were then filtered to retain only those that connect nodes
  within this regional subset, ensuring that the graph reflects the
  actual structure of the target area.\
  ]{.c8 .c9 .c11}

#### [5.4.3. Graph Construction]{.c8 .c1} {#h.ojphhmygbx0n .c23}

- [A ]{.c11}[weighted undirected graph]{.c7}[ was built using the
  filtered nodes and edges.\
  ]{.c8 .c9 .c11}
- [Nodes represent road intersections, and edges represent road segments
  (weighted by physical distance, although weight is not used in Degree
  Centrality calculation).\
  ]{.c8 .c9 .c11}

#### [5.4.4. Degree Centrality Computation]{.c8 .c1} {#h.8vhymw8s4p46 .c23}

- [For each node in the graph, the total number of direct neighbors
  (connected nodes) was counted.\
  ]{.c8 .c9 .c11}
- [This value was then normalized by dividing it by the maximum possible
  number of connections, i.e. N−1.\
  ]{.c8 .c9 .c11}
- [This yielded a normalized Degree Centrality value for each node,
  indicating its ]{.c11}[local importance or connectivity
  level]{.c7}[ within the network.\
  ]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

#### [5.4.5. Export to GeoJSON for Visualization]{.c8 .c1} {#h.vgzlzu8f16oz .c23}

- [The computed Degree Centrality values were added to the corresponding
  nodes along with their geographical coordinates.\
  ]{.c8 .c9 .c11}
- [The results were exported as a ]{.c11}[GeoJSON file]{.c7}[, which can
  be directly visualized in GIS tools such as ]{.c11}[QGIS]{.c7}[,
  allowing for spatial interpretation of node connectivity.]{.c8 .c9
  .c11}

[]{.c8 .c9 .c11}

[]{.c8 .c9 .c11}

### [5.5 PageRank Centrality]{.c8 .c19} {#h.2gfw8n7ob5ny .c5}

[PageRank Centrality]{.c25}[ is a node importance metric originally
developed by Google to rank web pages. In the context of transportation
networks, it measures the ]{.c11}[influence or popularity of a
node]{.c7}[ based on the number and quality of links it receives. A node
is considered important not only if many nodes point to it, but
especially if those pointing nodes are themselves important.]{.c8 .c9
.c11}

[The ]{.c11}[PageRank]{.c7}[ of a node v is given by the recursive
formula:]{.c8 .c9 .c11}

[![](images/image4.png){style="width: 311.00px; height: 73.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 311.00px; height: 73.00px;"}

[Where:]{.c8 .c9 .c11}

- [α is the ]{.c11}[damping factor]{.c7}[ (commonly set to 0.85), which
  represents the probability of continuing the navigation\
  ]{.c8 .c9 .c11}
- [N is the total number of nodes\
  ]{.c8 .c9 .c11}
- [M(v) is the set of nodes that link to node v\
  ]{.c8 .c9 .c11}
- [L(u) is the number of outgoing links from node u\
  ]{.c8 .c9 .c11}
- [The formula is iteratively updated until convergence\
  ]{.c8 .c9 .c11}

#### [Implementation Steps]{.c21 .c42} {#h.c0osjp86nj2k .c23}

[The PageRank computation is executed using a combination of
]{.c11}[Apache Spark]{.c7}[ for distributed preprocessing and a
]{.c11}[custom power iteration algorithm]{.c7}[ applied on a directed
graph structure. The steps are described below:]{.c8 .c9 .c11}

#### [5.5.1. Distributed Data Loading from HDFS using Spark RDDs]{.c8 .c1} {#h.mr20s3f6ohhl .c23}

- [The input files containing node coordinates and road segment data
  were stored on ]{.c11}[HDFS]{.c7}[ and loaded using ]{.c11}[Apache
  Spark]{.c7}[.\
  ]{.c8 .c9 .c11}
- [Both node and edge data were processed as ]{.c11}[RDDs]{.c7}[,
  allowing for efficient distributed parsing and filtering.\
  ]{.c8 .c9 .c11}

#### [5.5.2. Geographic Filtering of Nodes]{.c8 .c1} {#h.fd9s37gkg7u6 .c23}

- [Only nodes within the predefined ]{.c11}[Central Hong Kong
  Island]{.c7}[ region were retained for analysis.\
  ]{.c8 .c9 .c11}
- [This regional focus ensures that the PageRank scores reflect node
  influence ]{.c11}[within a specific urban area]{.c7}[ rather than the
  entire dataset.\
  ]{.c8 .c9 .c11}

#### [5.5.3. Construction of a Directed Graph]{.c8 .c1} {#h.jbc75ljvvmj2 .c23}

- [A ]{.c11}[directed graph]{.c7}[ was created using the filtered
  edges.\
  ]{.c8 .c9 .c11}
- [Each edge represents a directional connection between two
  intersections (e.g., due to one-way streets or typical traffic
  flows).\
  ]{.c8 .c9 .c11}
- [Although travel time was used in the input, for PageRank computation,
  only the graph ]{.c11}[structure (direction of connections)]{.c7}[ was
  considered, not the weights.\
  ]{.c8 .c9 .c11}

#### [5.5.4. PageRank Calculation using Power Iteration]{.c8 .c1} {#h.csde4b73x7nn .c23}

- [The PageRank algorithm was implemented manually using ]{.c11}[power
  iteration]{.c7}[, a common approach for solving eigenvector problems.\
  ]{.c8 .c9 .c11}
- [Initially, each node was assigned an equal score.\
  ]{.c8 .c9 .c11}
- [In each iteration, a node's new score was computed by ]{.c11}[summing
  contributions]{.c7}[ from its incoming neighbors, normalized by their
  number of outbound connections.\
  ]{.c8 .c9 .c11}
- [A damping factor α=0.85 was used to simulate the probability of
  following a link vs. randomly jumping to another node.\
  ]{.c8 .c9 .c11}
- [Iterations continued until the total change in scores (L1 norm of
  difference) fell below a small threshold, indicating
  ]{.c11}[convergence]{.c7}[.\
  ]{.c8 .c9 .c11}

#### [5.5.5. Output for Visualization]{.c8 .c1} {#h.7gr1j4a6krhc .c23}

- [Final PageRank values were merged with the node coordinates.\
  ]{.c8 .c9 .c11}
- [A ]{.c11}[GeoDataFrame]{.c7}[ was created and exported as a
  ]{.c11}[GeoJSON file]{.c7}[, making it directly usable for visual
  analysis in GIS software such as ]{.c11}[QGIS]{.c7}[.\
  ]{.c8 .c9 .c11}
- [This enables urban planners to ]{.c11}[visually identify the most
  influential intersections]{.c7}[ in the road network.]{.c11}

### []{.c8 .c12} {#h.c7t8juay7vbn .c5 .c24}

### []{.c8 .c12} {#h.t3zuj1vto2at .c5 .c24}

### []{.c8 .c12} {#h.i2zyv0xaopyg .c5 .c24}

### [6) Real-World Applications of Centrality Metrics]{.c8 .c12} {#h.udkwfezh032k .c5}

[]{.c8 .c1}

[6.1 Degree Centrality]{.c8 .c25 .c28}

[]{.c8 .c4 .c9}

[What areas require additional traffic signals or roundabouts to improve
flow efficiency?]{.c8 .c1}

[]{.c8 .c4 .c9}

[Degree Centrality measures how many direct connections (edges) a node
(intersection) has. Intersections with high Degree Centrality may
experience congestion due to their large number of connections. Adding
roundabouts or traffic signals to these points can help regulate flow
and improve safety. Since these nodes are central to many routes,
improvements here will have a broader impact on overall traffic
efficiency.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image53.png){style="width: 624.00px; height: 348.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 348.00px;"}

[Figure 1: Degree Centrality Visualization]{.c3}

[This visualization displays intersections with varying Degree
Centrality values, where ]{.c4}[dark red points]{.c1}[ represent
intersections with high Degree Centrality (highly connected) and
]{.c4}[lighter colors]{.c1}[ indicate lower connectivity. ]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image9.png){style="width: 624.00px; height: 348.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 348.00px;"}

[Figure 2: Recommended Roundabouts or Traffic Signals]{.c3}

[]{.c8 .c4 .c9}

[Based on the Degree Centrality analysis, ]{.c4}[roundabout
symbols]{.c1}[ are placed at intersections with the highest Degree
Centrality values. Implementing traffic control systems at these points
is recommended to enhance flow efficiency and safety, as disruptions at
these critical hubs can negatively affect the entire network.]{.c8 .c4
.c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[6.2 Closeness Centrality]{.c8 .c28 .c25}

[]{.c8 .c4 .c9}

[Where should emergency services (fire stations, hospitals) be located
for quick access?]{.c8 .c1}

[]{.c8 .c1}

[Closeness Centrality measures how quickly a node can reach all other
nodes in the network. High Closeness Centrality values indicate that a
node is centrally located, minimizing travel distance and time to other
parts of the network. Emergency services placed at these points can
respond more quickly to incidents across the entire network.]{.c8 .c4
.c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Where should emergency shelters be placed to ensure rapid accessibility
from multiple locations?]{.c8 .c1}

[]{.c8 .c1}

[Emergency shelters need to be easily accessible from a wide range of
locations. Nodes with high Closeness Centrality can be reached rapidly
from various points in the network, making them ideal locations for
emergency shelters to ensure maximum accessibility and safety during
disasters.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[What are the optimal locations for commercial centers to attract the
maximum foot traffic?]{.c8 .c1}

[]{.c8 .c4 .c9}

[Commercial centers benefit from being accessible from many different
parts of a network. High Closeness Centrality ensures that customers can
reach these locations quickly, encouraging higher foot traffic and
business efficiency.]{.c8 .c4 .c9}

[![](images/image20.png){style="width: 624.00px; height: 366.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 366.67px;"}[Figure
1: Closeness Centrality Visualization]{.c3}

[]{.c8 .c4 .c9}

[This visualization displays intersections based on their Closeness
Centrality values. ]{.c4}[Dark red points]{.c1}[ indicate intersections
with high Closeness Centrality, meaning they are well-connected and can
be quickly reached from various parts of the network. ]{.c4}[Dark blue
points]{.c1}[ represent intersections with low Closeness Centrality,
indicating longer travel distances to reach them. As seen in the map,
the most central locations are highlighted with dark red, confirming
that areas with high connectivity are concentrated in the core regions
of the network.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image45.png){style="width: 624.00px; height: 366.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 366.67px;"}

[Figure 2: Recommended Hospital Locations]{.c3}

[]{.c3}

[In this visualization, intersections with the highest Closeness
Centrality values are marked with ]{.c4}[hospital symbols]{.c1}[. These
points are ideal locations for hospitals due to their proximity to a
wide range of areas, ensuring quick access during medical
emergencies.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image26.png){style="width: 624.00px; height: 366.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 366.67px;"}

[Figure 3: Recommended Fire Station Locations]{.c3}

[]{.c8 .c4 .c9}

[This visualization highlights the same high Closeness Centrality
intersections but marked with ]{.c4}[fire station symbols]{.c1}[. These
locations are selected for their strategic positioning, allowing rapid
response to incidents across the network.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[6.3 Betweenness Centrality]{.c8 .c28 .c25}

[]{.c8 .c4 .c9}

[Where should major transit hubs (e.g., Bus Transfer Point) be
established for optimal connectivity?]{.c8 .c1}

[]{.c8 .c4 .c9}

[High Betweenness Centrality nodes lie on the shortest paths between
many pairs of nodes. Establishing transit hubs at these points allows
efficient routing and transfers, reducing congestion elsewhere and
enhancing overall network performance.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Which intersections should be prioritized for maintenance to prevent
widespread network failures?]{.c8 .c1}

[]{.c8 .c1}

[Betweenness Centrality identifies nodes that act as bridges or critical
transit points between different parts of the network. If these nodes
fail, a large portion of the network may become disconnected or
experience significant traffic disruptions. Prioritizing their
maintenance ensures the robustness and reliability of the entire
network.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[What intersections are most likely to cause congestion during peak
hours?]{.c8 .c1}

[]{.c8 .c4 .c9}

[Nodes with high Betweenness Centrality are often heavily used as
passage points. During peak hours, the heavy traffic passing through
these critical points can result in bottlenecks. Identifying these nodes
allows planners to implement measures to alleviate congestion.]{.c8 .c4
.c9}

[]{.c8 .c4 .c9}

[![](images/image12.png){style="width: 624.00px; height: 366.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 366.67px;"}

[Figure 1: Betweenness Centrality Visualization]{.c3}

[]{.c3}

[This visualization displays intersections based on their Betweenness
Centrality values. ]{.c4}[Darker blue points]{.c1}[ represent
intersections with higher Betweenness Centrality, indicating critical
points that frequently act as bridges between various parts of the
network. As the shade of blue darkens, the Betweenness Centrality
increases, highlighting essential transfer or transit points.]{.c8 .c4
.c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image18.png){style="width: 1786.47px; height: 1050.83px; margin-left: -124.69px; margin-top: -477.02px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 586.50px; height: 354.11px;"}

[Figure 2: Recommended Public Transportation Transfer Hubs]{.c3}

[]{.c8 .c4 .c9}

[In this visualization, ]{.c4}[bus symbols]{.c1}[ are placed on the
intersections with the highest Betweenness Centrality values. These
critical points act as major connectors within the network, making them
ideal locations for establishing public transportation transfer hubs to
optimize connectivity and improve overall efficiency.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image58.png){style="width: 624.00px; height: 366.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 366.67px;"}

[Figure 3: Potential Traffic Congestion Points]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[This visualization highlights intersections with high Betweenness
Centrality using ]{.c4}[traffic congestion symbols]{.c1}[. 30
intersections are marked, indicating areas likely to cause congestion
during peak hours. Because these points are frequently used as bridges
between different routes, traffic management measures should be
prioritized here to prevent bottlenecks and maintain network
efficiency.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[6.4 PageRank]{.c8 .c28 .c25}

[]{.c8 .c4 .c9}

[What are the most influential roads affecting overall traffic
flow?]{.c8 .c1}

[]{.c8 .c4 .c9}

[PageRank measures the importance of a node based on how many important
nodes connect to it. Roads that receive traffic from many influential
intersections are themselves influential. Identifying these roads helps
prioritize them for improvements, maintenance, or traffic management
interventions.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Where should promotional advertisements or billboards be placed?]{.c8
.c1}

[PageRank highlights nodes that attract attention from other influential
nodes. This makes it useful for finding locations where the maximum
number of people pass or have visibility. Placing advertisements or
billboards at high PageRank locations ensures greater exposure and
effectiveness.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image21.png){style="width: 624.00px; height: 366.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 366.67px;"}

[Figure 1: PageRank Visualization]{.c3}

[]{.c8 .c4 .c9}

[This visualization displays intersections based on their PageRank
values. ]{.c4}[Darker red points]{.c1}[ indicate intersections with
higher PageRank, meaning these points are considered more influential
within the network due to receiving connections from other important
intersections. As the shade of red darkens, the PageRank value
increases, highlighting the most prominent and popular
intersections.]{.c8 .c4 .c9}

[![](images/image44.png){style="width: 723.17px; height: 424.09px; margin-left: -99.67px; margin-top: -0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 623.50px; height: 388.84px;"}

[Figure 2: Recommended Billboard Locations]{.c3}

[]{.c8 .c4 .c9}

[In this visualization, ]{.c4}[billboard symbols]{.c1}[ are placed on
intersections with the highest PageRank values. These points are ideal
for ]{.c4}[advertising]{.c1}[ since they attract the most traffic and
visibility within the network. Placing billboards at these influential
intersections ensures maximum exposure to pedestrians and vehicles.]{.c8
.c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[6.5 Accessibility]{.c8 .c28 .c25}

[]{.c8 .c4 .c9}

[Which areas are underserved by existing infrastructure?]{.c8 .c1}

[]{.c8 .c4 .c9}

[Accessibility measures how easily nodes can be reached from various
points in the network. Nodes with low Accessibility values indicate
areas that are not well-connected, suggesting that infrastructure
improvements are necessary to increase accessibility and service
coverage.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[What intersections are least accessible, suggesting areas that require
additional road connections?]{.c8 .c1}

[]{.c8 .c4 .c9}

[By identifying nodes with poor Accessibility, urban planners can
determine which intersections or regions require additional connections.
Improving these nodes will enhance overall network connectivity and
ensure equitable access to resources.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Which areas are most vulnerable to isolation during disasters?]{.c8
.c1}

[]{.c8 .c4 .c9}

[Areas with low Accessibility are at greater risk of isolation during
natural disasters or infrastructure failures. Improving connections to
these areas increases their resilience and ensures that critical
services can reach them during emergencies.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image39.png){style="width: 624.00px; height: 366.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 366.67px;"}

[Figure 1: Accessibility Visualization]{.c3}

[]{.c8 .c4 .c9}

[This visualization displays intersections based on their Accessibility
values, where ]{.c4}[darker blue points]{.c1}[ indicate areas with
higher Accessibility. These points are more easily reachable from
various parts of the network, reflecting better connectivity and
integration within the urban layout. As the shade of blue darkens, the
Accessibility value increases.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[![](images/image37.png){style="width: 624.00px; height: 349.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 349.33px;"}

[Figure 2: Low Accessibility Areas Needing Improvement]{.c3}

[]{.c8 .c4 .c9}

[In this visualization, intersections with the ]{.c4}[lowest
Accessibility]{.c1}[ values are marked with ]{.c4}[city infrastructure
symbols]{.c1}[. These points are highlighted because they are less
connected to the rest of the network, indicating poor reachability and
inefficient connectivity.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Improving these low Accessibility areas is essential for enhancing
overall network performance and ensuring equitable access to resources
and services. Possible interventions include:]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

- [Building new roads or pathways to increase connectivity.]{.c8 .c4
  .c9}

[]{.c8 .c4 .c9}

- [Improving public transportation routes to include these underserved
  points.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

- [Creating alternative routes to prevent isolation during emergencies
  or natural disasters.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Addressing these issues will strengthen the network\'s resilience and
ensure more efficient transportation and service delivery throughout the
region.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[6.6 Extra Visualization: Edges]{.c8 .c28 .c25}

[]{.c8 .c4 .c9}

[![](images/image5.png){style="width: 624.00px; height: 349.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 349.33px;"}

[Figure 1: Road Network Visualization Based on Travel Time]{.c3}

[]{.c8 .c4 .c9}

[This visualization displays road segments with colors representing
]{.c4}[estimated travel times]{.c1}[:]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Red Lines]{.c1}[: Indicate high travel time or congested routes. These
segments likely experience heavy traffic or slow movement due to road
conditions or high usage.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Green Lines]{.c1}[: Indicate medium travel time. These routes maintain
moderate traffic flow and generally provide acceptable
connectivity.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[Blue Lines]{.c1}[: Indicate low travel time or free-flowing routes.
These segments have minimal traffic and offer the most efficient travel
conditions.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[The use of this visualization helps identify critical congestion
points, efficient routes, and potential areas for traffic improvement.
Road segments highlighted in red should be prioritized for interventions
to enhance traffic flow and reduce congestion.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

## [7) Results and Interpretation]{.c8 .c15} {#h.9fli1ph3sp7w .c32}

[In this study, five centrality metrics were calculated over the Central
Hong Kong Island road network to identify critical intersections,
evaluate infrastructure efficiency, and propose urban planning insights.
Each metric provided a unique perspective on the structure and dynamics
of the transportation network. The following section presents the
]{.c4}[interpretation of the results]{.c1}[, supported by ]{.c4}[spatial
visualizations]{.c1}[ and ]{.c4}[practical use-case
scenarios]{.c1}[.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

### [7.1 Degree Centrality -- Identifying Highly Connected Intersections]{.c8 .c19} {#h.maxl3m4dizuq .c5}

[The Degree Centrality analysis revealed which intersections have the
highest number of direct road connections. These nodes were visualized
using a red gradient, where ]{.c4}[darker red indicated higher
connectivity]{.c1}[. As expected, the most connected points were located
in central areas with dense road networks.]{.c8 .c4 .c9}

[In a second visualization, the ]{.c4}[top intersections]{.c1}[ were
marked with ]{.c4}[roundabout symbols]{.c1}[, suggesting they are ideal
locations for ]{.c4}[traffic signal upgrades]{.c1}[ or
]{.c4}[intersection redesign]{.c1}[. These spots serve as critical entry
and exit points and are more likely to experience frequent traffic
loads.]{.c8 .c4 .c9}

### []{.c8 .c1} {#h.z1y1hwce4ts5 .c5 .c24}

### []{.c8 .c19} {#h.2125kkycwlw1 .c5 .c24}

### []{.c8 .c19} {#h.ey01eg9qg2ls .c5 .c24}

### [7.2 Closeness Centrality -- Strategic Locations for Emergency Services]{.c8 .c19} {#h.kb9s4nb1c9ol .c5}

[Closeness Centrality values were visualized using a blue-to-red
gradient, where ]{.c4}[dark red nodes represented highly accessible
points]{.c1}[ that can quickly reach the rest of the network. As visible
in the map, these nodes were located centrally, highlighting their
importance in optimizing emergency response times.]{.c8 .c4 .c9}

[Two additional visualizations supported these findings:]{.c8 .c4 .c9}

- [High Closeness nodes marked with hospital icons]{.c1}[ suggested
  ideal placements for ]{.c4}[healthcare facilities]{.c1}[.\
  ]{.c8 .c4 .c9}
- [Fire station icons]{.c1}[ were also assigned to high Closeness nodes,
  reflecting ]{.c4}[fire response optimization]{.c1}[ based on travel
  efficiency.\
  ]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

### [7.3 Betweenness Centrality -- Transit Hubs and Congestion Risk Points]{.c8 .c19} {#h.6icaewjfj36s .c5}

[Betweenness Centrality uncovered intersections that lie on the
]{.c4}[shortest paths between other nodes]{.c1}[, thus acting as
critical ]{.c4}[transit or bottleneck points]{.c1}[. A darker blue color
indicated higher betweenness values in the map.]{.c8 .c4 .c9}

[Follow-up visualizations illustrated:]{.c8 .c4 .c9}

- [The ]{.c4}[top 3 intersections with bus icons]{.c1}[, suggesting
  locations for ]{.c4}[public transportation transfer hubs]{.c1}[.\
  ]{.c8 .c4 .c9}
- [Around ]{.c4}[30 intersections marked with traffic congestion
  icons]{.c1}[, indicating nodes likely to face ]{.c4}[peak-hour
  congestion]{.c1}[ and requiring ]{.c4}[traffic management
  attention]{.c1}[.\
  ]{.c8 .c4 .c9}

[These insights are crucial for infrastructure resilience and rerouting
strategies.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

### [7.4 PageRank -- Influence and Visibility within the Network]{.c8 .c19} {#h.dbyrzpswpwt2 .c5}

[PageRank values were visualized using a red gradient, with
]{.c4}[darker shades representing higher influence]{.c1}[. High PageRank
intersections are not only well connected but also ]{.c4}[connected to
other important nodes]{.c1}[, making them highly visible and frequently
visited.]{.c8 .c4 .c9}

[These nodes were emphasized with ]{.c4}[billboard icons]{.c1}[,
reflecting their suitability for ]{.c4}[advertisement
placement]{.c1}[ or ]{.c4}[commercial activity zones]{.c1}[. This data
can also support ]{.c4}[toll placement]{.c1}[, ]{.c4}[wayfinding
signage]{.c1}[, or ]{.c4}[public announcement systems]{.c1}[.]{.c8 .c4
.c9}

[]{.c8 .c4 .c9}

### [7.5 Accessibility Index -- Equity and Infrastructure Needs]{.c8 .c19} {#h.2og949z6zdv9 .c5}

[Accessibility was calculated as the sum of inverse travel times to a
node, reflecting how ]{.c4}[easily reachable]{.c1}[ an intersection is.
Nodes with high scores were shown in ]{.c4}[dark blue]{.c1}[, indicating
efficient network integration.]{.c8 .c4 .c9}

[In a dedicated map, nodes with ]{.c4}[the lowest Accessibility scores
were marked with infrastructure icons]{.c1}[. These represent
]{.c4}[underserved or disconnected regions]{.c1}[. Based on these
results, it is recommended to:]{.c8 .c4 .c9}

- [Extend or create road links to these points.\
  ]{.c8 .c4 .c9}
- [Improve public transport service coverage.\
  ]{.c8 .c4 .c9}
- [Evaluate disaster vulnerability and emergency access routes.\
  ]{.c8 .c4 .c9}

### []{.c8 .c19} {#h.ixlu3f5cea3o .c5 .c24}

### [7.6 Summary]{.c8 .c19} {#h.an4iv2dknm4o .c5}

[The combined use of multiple centrality metrics provided a rich and
multi-dimensional understanding of the Central Hong Kong Island road
network. Each metric highlighted a different form of node
importance---from connectivity and efficiency to influence and
vulnerability. The spatial visualizations supported concrete proposals
such as:]{.c8 .c4 .c9}

- [Transfer hub planning\
  ]{.c8 .c4 .c9}
- [Emergency service optimization\
  ]{.c8 .c4 .c9}
- [Congestion prevention\
  ]{.c8 .c4 .c9}
- [Equitable infrastructure development\
  ]{.c8 .c4 .c9}
- [Strategic advertisement positioning\
  ]{.c8 .c4 .c9}

[These findings demonstrate how data-driven network analysis can
directly inform ]{.c4}[urban planning, traffic management, and smart
city infrastructure design]{.c1}[.]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

[]{.c8 .c4 .c9}

### [8) Conclusion]{.c8 .c15} {#h.uwncipiu9wzz .c5}

[In this project, we analyzed the road network of ]{.c11}[Central Hong
Kong Island]{.c7}[ using five centrality metrics---]{.c11}[Degree,
Closeness, Betweenness, PageRank]{.c7}[, and
]{.c11}[Accessibility]{.c7}[---to uncover structurally important
intersections, traffic-critical nodes, and underserved regions. By
integrating ]{.c11}[distributed data processing with Apache
Spark]{.c7}[ and ]{.c11}[graph analytics]{.c7}[, we successfully
computed centrality scores over thousands of nodes and edges derived
from real-world geographic data.]{.c8 .c9 .c11}

[Each metric provided a distinct perspective:]{.c8 .c9 .c11}

- [Degree Centrality]{.c7}[ identified intersections with the highest
  number of direct connections, suggesting natural hubs for traffic
  management or control systems.\
  ]{.c8 .c9 .c11}
- [Closeness Centrality]{.c7}[ highlighted intersections with optimal
  reachability, supporting the placement of emergency services such as
  hospitals and fire stations.\
  ]{.c8 .c9 .c11}
- [Betweenness Centrality]{.c7}[ revealed key transit points likely to
  experience congestion, ideal for planning transfer hubs or rerouting
  schemes.\
  ]{.c8 .c9 .c11}
- [PageRank]{.c7}[ pinpointed influential nodes with high network
  visibility, useful for advertising or public service messaging.\
  ]{.c8 .c9 .c11}
- [Accessibility Index]{.c7}[ emphasized infrastructure equity, allowing
  detection of isolated regions in need of improved connectivity.\
  ]{.c8 .c9 .c11}

[Through ]{.c11}[QGIS visualizations]{.c7}[, we translated these
analytical results into actionable urban planning insights. By marking
key intersections with domain-specific symbols (e.g., hospitals,
billboards, roundabouts), we effectively communicated how network
centrality analysis can guide ]{.c11}[smart city decisions]{.c7}[.]{.c8
.c9 .c11}

[]{.c8 .c9 .c11}

[9) Literature Review: ]{.c8 .c15}

[]{.c8 .c19}

[Distributed Algorithms for Computation of Centrality Measures in
Complex Networks: ]{.c8 .c10}

- [This paper presents deterministic algorithms for computing degree,
  closeness, and betweenness centrality in a distributed manner. The
  algorithms work without prior knowledge of network size and are
  clock-free, making them suitable for large-scale dynamic networks.
  ]{.c3}

<!-- -->

- [[https://arxiv.org/abs/1507.01694](https://www.google.com/url?q=https://arxiv.org/abs/1507.01694&sa=D&source=editors&ust=1746730804909842&usg=AOvVaw1L9yCMB-6xbg44LFzTI7mP){.c37}]{.c33}[ ]{.c3}

[ ]{.c3}

[Computing Traffic Accident High-Risk Locations Using Graph Analytics:
]{.c8 .c10}

- [This research uses degree centrality and PageRank to identify and
  rank high-risk traffic accident locations. It develops a
  space-time-varying graph model, which can be applied to understand
  traffic congestion and accident-prone areas. ]{.c3}

<!-- -->

- [[https://arxiv.org/abs/2205.02851](https://www.google.com/url?q=https://arxiv.org/abs/2205.02851&sa=D&source=editors&ust=1746730804910835&usg=AOvVaw0v6vMUskVsvhO5t5xus-2e){.c37}]{.c33}[ ]{.c3}

[ ]{.c3}

[Graph-Based Analysis and Visualization of Mobility Data: ]{.c8 .c10}

- [This study explores how graph-based representations and centrality
  metrics can analyze urban mobility patterns. The paper applies
  centrality measures to mobility networks and visualizes structural
  properties, which can be useful for traffic flow analysis. ]{.c3}

<!-- -->

- [[https://arxiv.org/abs/2310.06732](https://www.google.com/url?q=https://arxiv.org/abs/2310.06732&sa=D&source=editors&ust=1746730804911769&usg=AOvVaw2V4zupcIkOD-wGLGA4YVZf){.c37}]{.c33}[ ]{.c3}

[]{.c8 .c9 .c11}

<div>

[]{.c3}

</div>
