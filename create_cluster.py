import argparse
import vertex_ray
from google.cloud import aiplatform
from vertex_ray import Resources

# CLUSTER_NAME: A name for the Ray on Vertex AI cluster that must be unique across your project.
# NETWORK is the full name of your peered VPC network, 
# in the format of projects/PROJECT_NUMBER/global/networks/VPC_NAME. PROJECT_NUMBER is your Google Cloud project number.


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Create Cluster")
    parser.add_argument(
        "--network", required=True, help="Network"
    )
    parser.add_argument(
        "--cluster", required=True, help="Cluster Name"
    )
    args, _ = parser.parse_known_args()

    print(f"Creating cluster with arguments cluster={args.cluster} - network={args.network}")

    # Define a default CPU cluster, machine_type is n1-standard-8, 1 head node and 1 worker node
    head_node_type = Resources()
    worker_node_types = [Resources()]

    # Or define a GPU cluster.
    head_node_type = Resources(
    machine_type="n1-standard-8",
    node_count=1,
    )

    worker_node_types = [Resources(
    machine_type="n1-standard-4",
    node_count=1,  # Can be > 1
    #   accelerator_type="NVIDIA_TESLA_K80",
    #   accelerator_count=1,
    )]

    # Initialize Vertex AI to retrieve projects for downstream operations.
    aiplatform.init()

    # Create the Ray on Vertex AI cluster
    CLUSTER_RESOURCE_NAME = vertex_ray.create_ray_cluster(
        head_node_type=head_node_type,
        network=args.network,
        worker_node_types=worker_node_types,
        python_version="3_10",  # Optional
        ray_version="2_4",  # Optional
        cluster_name = args.cluster
    )

    print(f"Cluster {args.cluster} created.")
